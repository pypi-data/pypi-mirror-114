"""Utilities for manipulating `torch.Tensor` tensors and arrays."""


import numpy as np
import torch


def to_tensor(obj, dtype=None, copy=False):
    """
    Creates a new `torch.Tensor` from the given array-like object
    (`numpy.ndarray`, `list`, etc.) while copying the underlying data.

    This differs from any of PyTorch's built-in functions to do this, in that
    when copying Python lists it won't reduce precision e.g. from float64 to
    float32.  In other words, this uses NumPy's type conversion semantics
    instead of PyTorch's, unless an explicit ``dtype`` argument is given.

    By default it avoids copying, unless ``copy=True``.  Even with
    ``copy=True`` sometimes copying is necessary (specifically when converting
    from Python types or when the existing dtype does not match the ``dtype``
    argument).
    """

    if not isinstance(obj, torch.Tensor):
        if not isinstance(obj, np.ndarray):
            if dtype is None:
                # Convert first to a NumPy array, e.g. if it's a Python
                # list--NumPy will prefer float64 over float32, unlike torch
                # which will convert floats to float32 by default, possibly
                # losing precision
                obj = np.array(obj)
            else:
                return torch.tensor(obj, dtype=dtype)

            # This results in initializing new storage for the Tensor in
            # the first place, so the additional clone() when copy=True
            # would be superfluous
            copy = False

        obj = torch.from_numpy(obj)
    elif dtype is None:
        # A bug I noticed in PyTorch: passing dtype=None can cause a segfault
        # (at least in the version I'm on 1.1.0; this might be fixed in a later
        # version), so if the dtype argument to this function is unspecified
        # just keep the original dtype
        dtype = obj.dtype

    return obj.detach().to(dtype=dtype, copy=copy)


def cut_and_cat(tensor1, tensor2):
    """
    To describe.
    """
    if tensor1.size() == torch.Tensor([]).size():
        return tensor2
    elif tensor2.size() == torch.Tensor([]).size():
        return tensor1
    dif = tensor1.size(2) - tensor2.size(2)

    if dif > 0:
        return torch.cat((tensor1[:, :, (dif // 2):(-dif // 2)], tensor2), 1)
    elif dif < 0:
        return torch.cat((tensor1, tensor2[:, :, (-dif // 2):(dif // 2)]), 1)
    else:
        return torch.cat((tensor1, tensor2), 1)


def nanmean(v, *args, inplace=False, **kwargs):
    """
    Compute mean while ignoring NaNs.

    Additional arguments are passed to the underlying ``.sum()`` calls; e.g. to
    compute the mean along a specific dimension.

    Thanks to Yul Kang for this recipe:
    https://github.com/pytorch/pytorch/issues/21987#issuecomment-539402619

    Examples
    --------

    >>> from dnadna.utils.tensor import nanmean
    >>> import torch
    >>> nan = float('nan')
    >>> t = torch.tensor([1.0, 2.0, nan, 3.0])
    >>> nanmean(t).item()
    2.0
    >>> t = torch.tensor([
    ...     [1.0, nan],
    ...     [2.0, 4.0],
    ...     [nan, nan],
    ...     [3.0, 5.0]])
    >>> nanmean(t, 0)
    tensor([2.0000, 4.5000])
    >>> nanmean(t, 1).squeeze()
    tensor([1., 3., nan, 4.])

    .. note::

        In the last example a NaN is still included in the output since the
        only meaningful mean for that row is NaN, but rows that contained
        non-NaN values still have a NaN-excluded mean.
    """

    if isinstance(v, np.ndarray):
        v = torch.from_numpy(v)
    elif not isinstance(v, torch.Tensor):
        v = torch.tensor(v)

    if not inplace:
        v = v.clone()
    is_nan = torch.isnan(v)
    v[is_nan] = 0
    return v.sum(*args, **kwargs) / (~is_nan).float().sum(*args, **kwargs)
