import numpy as np
import pandas as pd
import pytest
import torch

from dnadna import DNADNAWarning
from dnadna.datasets import DictSNPSource, DNATrainingDataset
from dnadna.params import LearnedParams
from dnadna.snp_sample import SNPSample
from dnadna.transforms import ReformatPosition, Transform


@pytest.fixture
def test_dataset(monkeypatch):
    # The Subsample transform uses np.random.choice to determine which
    # rows/individuals to subsample, so we monkeypatch it to always give
    # a deterministic result for the test
    monkeypatch.setattr(np.random, 'choice',
                        lambda *args, **kwargs: np.array([0, 2]))

    # The Rotate transform uses np.random.randint to determine how many
    # positions to rotate by
    monkeypatch.setattr(np.random, 'randint',
                        lambda *args, **kwargs: 1)

    snp = SNPSample(
        snp=[[1, 0, 1, 0], [0, 1, 1, 1], [1, 1, 0, 0]],
        pos=[0.1, 0.2, 0.6, 0.8]
    )

    source = DictSNPSource({(0, 0): snp, (1, 0): snp})

    # One parameter tied to position so we can test that it gets rotated
    params = {
        'position': {
            'type': 'regression',
            'tied_to_position': True
        }
    }

    scenario_params = pd.DataFrame({
        'scenario_idx': [0, 1],
        'position': [0.42, 0.42],
        'n_replicates': [1, 1],
        'splits': ['training', 'validation']
    })

    learned_params = LearnedParams(params, scenario_params)

    return DNATrainingDataset(validate=False, source=source,
                              learned_params=learned_params)


def test_transforms(test_dataset):
    """
    Test that transforms are applied correctly to items loaded from the
    `dnadna.dna_loader.DNATrainingDataset`.
    """

    test_dataset.transforms = [
        {'reformat_position': {'distance': True}},
        {'subsample': 2}
    ]

    _, _, snp_sample, scenario = test_dataset[0]
    # The snp_matrix should be reformated to distance, subsampled from the 0th
    # and 2nd individuals
    expected = torch.tensor([
        [0.2, 0.4],
        [  0,   1],  # noqa: E201,E241
        [  1,   0]  # noqa: E201,E241
    ], dtype=torch.double)

    # There is a tiny amount of difference from floating point rounding
    assert torch.allclose(snp_sample.tensor, expected)

    # The 'position' parameter should have remained untouched
    assert np.allclose(scenario[0].item(), 0.42)


def test_dataset_split_transforms(test_dataset):
    """
    Test applying different transforms depending on the dataset split.
    """

    test_dataset.transforms = {
        'training': [
            {'crop': {'max_snp': 2, 'keep_polymorphic_only': False}}
        ],
        'validation': [
            {'crop': {'max_indiv': 2, 'keep_polymorphic_only': False}}
        ]
    }

    _, _, snp_sample, _ = test_dataset[0]

    # The snp_matrix should be cropped to just 2 snps
    expected = torch.tensor([
        [0.1, 0.2],
        [  1,   0],  # noqa: E201,E241
        [  0,   1],  # noqa: E201,E241
        [  1,   1]  # noqa: E201,E241
    ], dtype=torch.double)

    assert (snp_sample.tensor == expected).all()

    _, _, snp_sample, _ = test_dataset[1]
    # This one is in the validation set, so we should expect the number of
    # individuals to be cropped to 2
    expected = torch.tensor([
        [0.1, 0.2, 0.6, 0.8],
        [  1,   0,   1,   0],  # noqa: E201,E241
        [  0,   1,   1,   1]  # noqa: E201,E241
    ], dtype=torch.double)

    assert (snp_sample.tensor == expected).all()


def test_transforms_rotate_crop(test_dataset):
    """
    Test that transforms are applied correctly to items loaded from the
    `dnadna.dna_loader.DNATrainingDataset`.
    """

    test_dataset.transforms = [
        {'reformat_position': {'circular': True, 'distance': True}},
        {'crop': {'max_indiv': 2, 'keep_polymorphic_only': False}},
        'Rotate'
    ]

    _, _, snp_sample, scenario = test_dataset[0]
    # The snp_matrix should be reformated to distance and circular mode
    # cropped to the first 2 individuals, with all columns kept even if not polymorphic anymore
    # then rotated (here the shift is one towards the right)
    expected = torch.tensor([
        [0.2, 0.3, 0.1, 0.4],
        [  0,  1,   0,  1],  # noqa: E201,E241
        [  1,  0,   1,  1]  # noqa: E201,E241
    ], dtype=torch.double)

    # There is a tiny amount of difference from floating point rounding
    assert torch.allclose(snp_sample.tensor, expected)

    # The 'position' parameter should also have been shifted by the
    # rotation
    # TODO: I think this should only be done in the case of circular distances
    # but I need to double-check
    assert np.allclose(scenario[0].item(), 0.22)


def test_broken_transform(test_dataset):
    """
    Test that a warning is raised when loading a broken transform and that
    the sample will be excluded.
    """

    class BogusTransform(Transform):
        def __call__(self, data):
            1 / 0

    test_dataset.transforms = [BogusTransform()]

    with pytest.warns(DNADNAWarning,
            match=r"an exception occurred evaluating BogusTransform\(\) on "
                  r"scenario 0 replicate 0: ZeroDivisionError\('division by "
                  r"zero'\)"):
        _, _, sample, scenario = test_dataset[0]

    assert sample is None


def test_random_transforms():
    """
    Applies a random sequence of many different position transformations, and
    ensures that at the end we can still transform back to the original
    position format with minimal loss (there will be a small difference due
    only to rounding errors).
    """

    np.random.seed(0)
    torch.random.manual_seed(0)

    # We start with a random SNP matrix with normalized positions in a
    # chromosome of size 2000000
    # We choose normalized positions to start with, because after many
    # transformations there may be a little loss due to rounding.  In the end
    # we will want to perform an allclose (relative) comparison, which is
    # harder to do with integers where rounding could cause a bit of whole
    # integer drift.
    snp = torch.rand((50, 400)) < 0.5
    # Ensure that the normalized positions properly scale to full integers
    # when de-normalized
    pos = torch.rand(400, dtype=torch.double).sort().values
    pos = (pos * 2e6).round() / 2e6
    orig_pos_format = {
            'normalized': True,
            'distance': False,
            'circular': False,
            'chromosome_size': 2e6,
            'initial_position': pos[0].item()
    }
    orig_sample = sample = SNPSample(snp, pos, pos_format=orig_pos_format)
    transforms = []

    for _ in range(100):
        # Apply 100 random transforms
        prev_sample = sample
        pos_format = {
            'distance': bool(np.random.randint(0, 2)),
            'normalized': bool(np.random.randint(0, 2)),
            'circular': bool(np.random.randint(0, 2))
        }
        transform = ReformatPosition(**pos_format)
        transforms.append(transform)
        sample, _, _ = transform((prev_sample, None, None))

        # Ensure we can transform back to the previous format
        prev_transform = ReformatPosition(**prev_sample.full_pos_format)
        sample2, _, _ = prev_transform((sample, _, _))
        assert prev_sample.full_pos_format == sample2.full_pos_format
        assert torch.allclose(prev_sample.pos, sample2.pos)

    # Convert back to the original format
    transform = ReformatPosition(**orig_pos_format)
    sample, _, _ = transform((sample, None, None))
    assert torch.allclose(orig_sample.pos, sample.pos)
