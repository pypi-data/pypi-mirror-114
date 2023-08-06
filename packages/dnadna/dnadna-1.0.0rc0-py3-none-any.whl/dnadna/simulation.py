"""Implements container for DNADNA-compatible simulation datasets."""


from .datasets import DNADataset


class Simulation(DNADataset):
    """
    Class representing a specific simulation, consisting of a data source for
    the simulated SNPs, and a table of scenario parameters.
    """

    config_schema = 'simulation'
