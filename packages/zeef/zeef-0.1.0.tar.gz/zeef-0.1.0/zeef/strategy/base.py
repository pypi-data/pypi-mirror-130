"""
    Pool-based active learning strategy base class.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 07/12/2021
"""

from tqdm import tqdm

import torch
import torch.optim as optim
import torch.nn.functional as F


class Strategy:
    def __init__(self, data_pool, net, args):
        self.args = args
        self.data_pool = data_pool
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net = net().to(self.device)

    def query(self, number):
        """
        The query function that calls the specific active learning strategy.
        :param number: the query number.
        :return: the data ids in a numpy array.
        """
        pass

    def query_object(self, number):
        """
        The query function that calls the specific active learning strategy.
        :param number: the query number.
        :return: the data points in a numpy array.
        """
        pass

    def update(self, labeled_ids, labels):
        """
        Update the data pool with labels.
        :param labeled_ids: the ids of labeled data.
        :param labels: the corresponding data labels.
        :return: None
        """
        self.data_pool.label(labeled_ids, labels)

    def _train(self, loader_train, optimizer):
        # TODO: needs refactor
        self.net.train()
        for _, (x, y, _) in tqdm(enumerate(loader_train)):
            x, y = x.to(self.device), y.to(self.device)
            optimizer.zero_grad()
            out = self.net(x)
            loss = F.cross_entropy(out, y)
            loss.backward()
            optimizer.step()

    def learn(self):
        # TODO: needs refactor
        n_epoch = self.args['n_epoch']
        optimizer = optim.SGD(self.net.parameters(), **self.args['optimizer_args'])
        loader_train = self.data_pool.get_train_loader(64)

        for _ in range(n_epoch):
            self._train(loader_train, optimizer)

    def predict(self, data_x, data_y):
        # TODO: needs refactor
        loader_test = self.data_pool.get_dataloader(data_x, data_y, 1000)

        self.net.eval()
        predictions = torch.zeros(len(data_y), dtype=data_y.dtype)
        with torch.no_grad():
            for x, y, idxs in loader_test:
                x, y = x.to(self.device), y.to(self.device)
                out = self.net(x)
                pred = out.max(1)[1]
                predictions[idxs] = pred.cpu()

        return predictions

    def infer(self, data_y):
        # TODO: needs refactor
        self.net.eval()
        data_y = self.data_pool.transform(data_y)
        input_tensor = data_y.to(self.device)
        with torch.no_grad():
            outputs = self.net(input_tensor)
            if isinstance(outputs, tuple):
                return outputs[0].cpu().detach()
            else:
                return outputs.cpu().detach()
