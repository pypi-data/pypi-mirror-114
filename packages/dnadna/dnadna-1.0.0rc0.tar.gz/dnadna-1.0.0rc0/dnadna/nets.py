# -*- coding: utf-8 -*-
"""DNADNA's neural nets used for model training."""


import abc

import numpy as np

import torch
import torch.nn as nn
import logging
from torch.nn.functional import relu

from .utils.plugins import Pluggable, gen_name_params_schema
from .utils.tensor import cut_and_cat


log = logging.getLogger(__name__)


class Network(nn.Module, Pluggable, metaclass=abc.ABCMeta):
    """
    Base class for DNADNA neural nets.

    All neural nets, including user-defined neural nets in plugins, must
    use this base class, as it adds the net to the registry of nets known by
    the software.  Sub-modules used by the net but that are not meant for use
    on their own should still use `torch.nn.Module` as their base class.
    """

    schema = {}
    """
    Schema for the network's ``net_params``, the section in the training config
    for parameters the net instance should be instantiated with (e.g.
    ``n_snp``, ``n_indiv`` in the case of `SPIDNA1`, among others).

    It can be either a string containing the name (without the ``.yml``
    extension) of a schema in the default schema path (for built-in nets) or
    a `dict` representing the schema.

    If left empty, the ``net_params`` simply won't be validated when loading
    the config.
    """

    _computed_params = set(['n_snp', 'n_indiv', 'n_outputs', 'concat'])
    """
    These are some special network initialization parameters which, if not
    specified in the network's configuration, are computed at runtime based on
    the dataset.  See ModelTrainer._prepare_net.
    """

    @abc.abstractproperty
    def forward(self, x):
        """
        The forward function of the network (see `torch.nn.Module` for more
        details).  Should accept a batch of SNP matrices as input (may be
        in either concat format (where the position array has the SNP matrix
        concatenated to it) or product format (where the position array is
        multiplied by the SNP matrix).

        If the operation of the net depends on which format the input is in,
        its ``__init__`` method should accept a ``concat`` argument.  It will
        be passed `True` or `False` by the network trainer depending on which
        format the inputs are in.
        """

    @classmethod
    def get_schema(cls):
        """
        Returns a schema pairing the ``network.name`` property with the valid
        ``network.params`` associated with that network (which may be very
        broad if the `Network` subclass does not specify its `Network.schema`).
        """

        if cls is not Network:
            # This is a Network plugin; just return the net's config schema
            return cls.schema

        return gen_name_params_schema(cls, cls._computed_params)


DNADNANet = Network
"""
Alias for backwards-compatibility; use just `dnadna.nets.Network` instead.
"""


class SPIDNABlock(nn.Module):
    """
    Sub-part of the SPIDNA network. The number of SPIDNABlock inside the
    SPIDNA network is defined by the n_blocks parameter.
    """
    def __init__(self, n_outputs, n_features):
        super().__init__()
        self.n_outputs = n_outputs
        self.phi = nn.Conv2d(n_features * 2, n_features, (1, 3))
        self.phi_bn = nn.BatchNorm2d(n_features * 2)
        self.maxpool = nn.MaxPool2d((1, 2))
        self.fc = nn.Linear(n_outputs, n_outputs)

    def forward(self, x, output):
        x = self.phi(self.phi_bn(x))
        psi1 = torch.mean(x, 2, keepdim=True)
        psi = psi1
        current_output = self.fc(torch.mean(psi[:, :self.n_outputs, :, :], 3).squeeze(2))
        output += current_output
        psi = psi.expand(-1, -1, x.size(2), -1)
        x = torch.cat((x, psi), 1)
        x = relu(self.maxpool(x))
        return x, output


class SPIDNA(Network):
    """
    SPIDNA is a convolutional neural network that infers evolutionary
    parameters.

    This network's predictions are invariant to the permutation of individuals
    in the SNP matrix and adaptive to the number of individuals.

    It is also adaptive to the number of SNPs, although it is recommended to
    evaluate the performance when the number of SNPs varies, because batch
    normalization is applied.

    Task
    ----
    Regression

    Constraints
    -----------
    min_snp : 400
    max_snp : no constraint
    min_indiv : 2
    max_indiv : no constraint

    Warnings
    ----------
    None

    Notes
    ------
    This net has been used to predict population sizes through time.

    It is called "SPIDNA batch normalization" in Sanchez et al. 2020 and was
    trained with data cropped to a fixed number of SNPs (400) and individuals
    (50) without padding. However this is not a constraint of the architecture,
    which is adaptive to the number of individuals and SNPs.

    Publication
    -----------
    T. Sanchez, J. Cury, G. Charpiat, et F. Jay,
    « Deep learning for population size history inference: Design, comparison and
    combination with approximate Bayesian computation »,
    Mol Ecol Resour, p. 1755‑0998.13224, juill. 2020, doi: 10.1111/1755-0998.13224.

    Parameters
    ----------
    n_blocks : int
        number of SPIDNA blocks in the architecture
    n_features: int
        number of convolution filters in each convolution layer, doubled for
        layers inside SPIDNA blocks
        n_features should be greater or equal to n_outputs.
    n_outputs : int
        number of demographic parameters to infer
    """

    schema = 'nets/spidna'

    def __init__(self, n_blocks, n_features, n_outputs):
        super().__init__()
        self.n_outputs = n_outputs
        self.conv_pos = nn.Conv2d(1, n_features, (1, 3))
        self.conv_pos_bn = nn.BatchNorm2d(n_features)
        self.conv_snp = nn.Conv2d(1, n_features, (1, 3))
        self.conv_snp_bn = nn.BatchNorm2d(n_features)
        self.blocks = nn.ModuleList([SPIDNABlock(n_outputs, n_features)
                                     for i in range(n_blocks)])

    def forward(self, x):
        pos = x[:, 0, :].view(x.shape[0], 1, 1, -1)
        snp = x[:, 1:, :].unsqueeze(1)
        pos = relu(self.conv_pos_bn(self.conv_pos(pos)))
        pos = pos.expand(-1, -1, snp.size(2), -1)
        snp = relu(self.conv_snp_bn(self.conv_snp(snp)))
        x = torch.cat((pos, snp), 1)
        output = torch.zeros(x.size(0), self.n_outputs, device=x.device)
        for block in self.blocks:
            x, output = block(x, output)
        return output


class CustomCNN(Network):
    """
    CustomCNN is a convolutional neural network that infers demographic
    parameters from a SNP matrix and its associated vector of positions. The
    number of SNP is predefined and fixed.

    The network is based on multiple 2D convolution filters of mixed sizes.

    Task
    ----
    Regression

    Constraints
    -----------
    min_snp : 400
    max_snp : no constraint
    min_indiv : 50
    max_indiv : 50

    Warnings
    ----------
    None

    Notes
    ------
    This net was used to predict population sizes through time.
    It is called "custom CNN" in Sanchez et al., and was referred to in earlier
    versions of this code as "SPIDNA1".

    Publication
    -----------
    T. Sanchez, J. Cury, G. Charpiat, et F. Jay,
    « Deep learning for population size history inference: Design, comparison and
    combination with approximate Bayesian computation »,
    Mol Ecol Resour, p. 1755‑0998.13224, juill. 2020, doi: 10.1111/1755-0998.13224.

    Parameters
    ----------
    n_snp : int
        number of SNPs in the alignment data
    n_indiv : int
        number of individuals in the SNP data
    n_outputs : int
        number of demographic parameters to infer
    concat: bool
        Whether the position vector is concatenated to the SNP matrix.
        Thus, it adds 1 to the dimension of the individuals.


    """

    schema = 'nets/custom_cnn'

    def __init__(self, n_snp, n_indiv, n_outputs, concat=True):
        super().__init__()
        self.n_indiv = n_indiv
        self.concat = True
        self.filters = [(2, 2), (5, 4), (3, 8), (2, 10), (20, 1)]
        self.outputs_height = [20 * (20 - x + 1) + 5
                               for x in [2, 5, 3, 2, 20]]
        self.outputs_height_cumsum = [0] + [
            int(x) for x in np.cumsum(self.outputs_height)]

        self.conv1 = nn.ModuleList()
        self.batch_norm1 = nn.ModuleList()
        self.conv2 = nn.ModuleList()
        self.batch_norm2 = nn.ModuleList()
        self.conv3 = nn.ModuleList()
        self.batch_norm3 = nn.ModuleList()

        for idx, filt in enumerate(self.filters):
            self.conv1.append(nn.Conv1d(1, 5, filt[1]))
            self.batch_norm1.append(nn.BatchNorm1d(5))
            self.conv2.append(nn.Conv2d(1, 20, filt))
            self.batch_norm2.append(nn.BatchNorm2d(20))
            self.conv3.append(nn.Conv2d(1, 50, (self.outputs_height[idx], 1)))
            self.batch_norm3.append(nn.BatchNorm2d(50))

        self.conv4 = nn.Conv2d(1, 50, (250, 1))
        self.batch_norm4 = nn.BatchNorm2d(50)

        self.conv5 = nn.Conv2d(1, 50, (50, 3), stride=3)
        self.batch_norm5 = nn.BatchNorm2d(50)

        self.conv6 = nn.Conv2d(1, 50, (50, 3), stride=3)
        self.batch_norm6 = nn.BatchNorm2d(50)

        self.conv7 = nn.Conv2d(1, 50, (50, 3), stride=3)
        self.batch_norm7 = nn.BatchNorm2d(50)

        self.conv8 = nn.Conv2d(1, 50, (50, 3), stride=3)
        self.batch_norm8 = nn.BatchNorm2d(50)

        # TODO: This crashes if n_snp is too low (you end up with 0 inputs
        # for the Linear transform).  We need better input validation for the
        # models.
        self.fc1 = nn.Linear(50 * ((n_snp - 10 + 1) // 3 // 3 // 3 // 3), 50)
        self.batch_norm9 = nn.BatchNorm1d(50)

        self.fc2 = nn.Linear(50, n_outputs)

    def forward(self, x):
        batch_size = x.size(0)
        x = x.unsqueeze(1)
        x1 = x[:, :, 0, :].contiguous()
        x2 = x[:, :, 1:(self.n_indiv + int(self.concat)), :].contiguous()
        big_x = torch.Tensor()

        for f in range(len(self.filters)):
            x1_tmp = self.conv1[f](x1)
            x1_tmp = relu(self.batch_norm1[f](x1_tmp))
            x2_tmp = self.conv2[f](x2)
            x2_tmp = relu(self.batch_norm2[f](x2_tmp))
            x2_tmp = x2_tmp.view(batch_size, x2_tmp.size(1) * x2_tmp.size(2),
                                 x2_tmp.size(3))
            big_x = cut_and_cat(big_x, torch.cat((x1_tmp, x2_tmp), 1))

        big_x = big_x.unsqueeze(1)

        def apply_relu_batch_norm(f):
            # TODO: Better name for this?  I'm not sure
            output_low = self.outputs_height_cumsum[f]
            output_hi = self.outputs_height_cumsum[f + 1]
            filt = relu(self.batch_norm3[f](
                self.conv3[f](big_x[:, :, output_low:output_hi, :])))
            return filt.squeeze(2)

        big_x = torch.cat([apply_relu_batch_norm(f)
                           for f in range(len(self.filters))], 1).unsqueeze(1)

        big_x = self.conv4(big_x)
        big_x = relu(self.batch_norm4(big_x)).squeeze(2).unsqueeze(1)

        big_x = self.conv5(big_x)
        big_x = relu(self.batch_norm5(big_x)).squeeze(2).unsqueeze(1)

        big_x = self.conv6(big_x)
        big_x = relu(self.batch_norm6(big_x)).squeeze(2).unsqueeze(1)

        big_x = self.conv7(big_x)
        big_x = relu(self.batch_norm7(big_x)).squeeze(2).unsqueeze(1)

        big_x = self.conv8(big_x)
        big_x = relu(self.batch_norm8(big_x))

        big_x = big_x.view(big_x.size(0), -1)

        big_x = self.fc1(big_x)
        big_x = relu(self.batch_norm9(big_x))

        big_x = self.fc2(big_x)

        return big_x


class MLP(Network):
    """

    MLP is a basic fully connected network.
    It can be used as a baseline or for testing dnadna.

    Task
    ----
    Regression / Classification

    Constraints
    -----------
    min_snp : no constraints
    max_snp : no constraints
    min_indiv : no constraints
    max_indiv : no constraints

    Warnings
    ----------
    None

    Parameters
    ----------
    n_snp : int
        number of SNPs in the alignment data
    n_indiv : int
        number of individuals in the SNP data
    n_outputs : int
        number of parameters or classes to infer
    concat: bool
        Whether the position vector is concatenated to the SNP matrix.
        Thus, it adds 1 to the dimension of the individuals.

    """

    schema = 'nets/mlp'

    def __init__(self, n_snp, n_indiv, n_outputs, concat=True):
        super().__init__()
        # an affine operation: y = Wx + b
        # # SNP * (indiv + 1)  (1 for positions)
        n_samples = n_indiv + int(concat)
        self.fc1 = nn.Linear(n_snp * n_samples, 100)
        self.fc2 = nn.Linear(100, 50)
        self.fc3 = nn.Linear(50, 5)
        self.fc4 = nn.Linear(5, n_outputs)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = relu(self.fc1(x))
        x = relu(self.fc2(x))
        x = relu(self.fc3(x))
        x = self.fc4(x)
        return x

    def num_flat_features(self, x):
        # log.debug(f"num_flat_features, {x.shape}")
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


class CNN(Network):
    """

    CNN is a basic convolutional neural network.
    It can be used as a baseline or for testing dnadna

    Task
    ----
    Regression / Classification

    Constraints
    -----------
    min_snp : 400
    max_snp : 400
    min_indiv : 50
    max_indiv : 50

    Warnings
    ----------
    None

    Parameters
    ----------
    n_outputs : int
        number of parameters or classes to infer

    """

    schema = 'nets/cnn'

    def __init__(self, n_outputs):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 5, kernel_size=3, stride=2, bias=False)
        self.bn1 = nn.BatchNorm2d(5)
        self.pool = nn.MaxPool2d(2, 2)

        self.conv2 = nn.Conv2d(5, 10, kernel_size=3, stride=2, bias=False)
        self.fc1 = nn.Linear(480, 10)  # constraint for 400 snp and 50 indiv.
        self.fc2 = nn.Linear(10, 5)
        self.fc3 = nn.Linear(5, n_outputs)

    def forward(self, x):
        batch_size = x.size(0)
        x = x.unsqueeze(1)
        x = self.pool(relu(self.conv1(x)))
        x = self.bn1(x)
        x = self.pool(relu(self.conv2(x)))
        x = x.view(batch_size, -1)  # flatten the tensor for each batch element
        x = relu(self.fc1(x))
        x = relu(self.fc2(x))
        x = self.fc3(x)
        return x
