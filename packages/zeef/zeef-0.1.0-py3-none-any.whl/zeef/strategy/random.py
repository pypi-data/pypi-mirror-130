"""
    Random sampling methods.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 06/12/2021
"""

import numpy as np
from .base import Strategy


class RandomSampling(Strategy):
    """
    Randomly Selected the query samples.
    """

    def __init__(self, data_pool, net, args):
        super(RandomSampling, self).__init__(data_pool, net, args)

    def query(self, number):
        return np.random.choice(list(self.data_pool.get_unlabeled_ids()), number, replace=False)
