"""
    Uncertainty based sampling methods.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 08/12/2021
"""

import torch
from .base import Strategy


class LeastConfidence(Strategy):
    def __init__(self, data_pool, net, args):
        super(LeastConfidence, self).__init__(data_pool, net, args)

    def query(self, n):
        unlabeled_data = self.data_pool.get_unlabeled_data()
        unlabeled_ids = self.data_pool.get_unlabeled_ids()
        probs = self.infer(unlabeled_data)
        uncertainties = probs.max(1)[0]
        return unlabeled_ids[uncertainties.sort()[1][:n]]


class MarginConfidence(Strategy):
    def __init__(self, data_pool, net, args):
        super(MarginConfidence, self).__init__(data_pool, net, args)

    def query(self, n):
        unlabeled_data = self.data_pool.get_unlabeled_data()
        unlabeled_ids = self.data_pool.get_unlabeled_ids()
        probs = self.infer(unlabeled_data)
        probs_sorted, _ = probs.sort(descending=True)
        difference_list = probs_sorted[:, 0] - probs_sorted[:, 1]
        return unlabeled_ids[difference_list.sort()[1][:n]]


class RatioConfidence(Strategy):
    def __init__(self, data_pool, net, args):
        super(RatioConfidence, self).__init__(data_pool, net, args)

    def query(self, n):
        unlabeled_data = self.data_pool.get_unlabeled_data()
        unlabeled_ids = self.data_pool.get_unlabeled_ids()
        probs = self.infer(unlabeled_data)
        probs_sorted, _ = probs.sort(descending=True)
        difference_list = probs_sorted[:, 0] / probs_sorted[:, 1]
        return unlabeled_ids[difference_list.sort()[1][:n]]


class EntropySampling(Strategy):
    def __init__(self, data_pool, net, args):
        super(EntropySampling, self).__init__(data_pool, net, args)

    def query(self, n):
        unlabeled_data = self.data_pool.get_unlabeled_data()
        unlabeled_ids = self.data_pool.get_unlabeled_ids()
        predictions = self.infer(unlabeled_data)
        entropy = (predictions * torch.log(predictions)).sum(1)
        return unlabeled_ids[entropy.sort()[1][:n]]
