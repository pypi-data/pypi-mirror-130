"""
    The basic data management class for both pool and stream based AL methods.
    @author huangyz0918 (huangyz0918@gmail.com)
    @date 05/12/2021
"""

import numpy as np
from PIL import Image

from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms


class TorchDataset(Dataset):
    """
    TorchDataset: a base PyTorch dataset. TODO: need refactor, extract the data processing function.
    """

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    def __getitem__(self, index):
        x, y = self.X[index], self.Y[index]
        x = Image.fromarray(x.numpy(), mode='L')
        x = self.transform(x)
        return x, y, index

    def __len__(self):
        return len(self.X)


class Pool:
    """
    Data Pool for pool-based query strategies.
    """

    def __init__(self, raw_data, transform=None):
        self.transform = transform
        self.data = raw_data
        self.size = len(self.data)
        self.labels = np.empty(len(self.data), dtype=object)
        self.labeled_ids = set()

    def get_unlabeled_data(self):
        """
        Get the unlabeled data.
        :return: numpy array of unlabeled data objects.
        """
        return np.delete(self.data, list(self.labeled_ids), 0)

    def get_unlabeled_ids(self):
        """
        Get the unlabeled data ids, used for query in the unlabeled data pool.
        :return: a list (numpy array) contains all the unlabeled data ids.
        """
        return np.delete(range(self.size), list(self.labeled_ids))

    def label_by_ids(self, label_index_list, labels):
        """
        Label the data by given data ids, those ids should be existed in the given total
        data pool. The labels is a list of labels for corresponding indexed data points.

        :param label_index_list: a list of data ids.
        :param labels: a list of labels.
        :return: None
        """
        if len(label_index_list) == len(labels):
            self.labeled_ids.update(label_index_list)
            self.labels[label_index_list] = labels
        else:
            raise ValueError("the labeled data number should be the same as the corresponding labels.")

    def label_by_id(self, label_index, y):
        """
        Label single data point by indexing the data location.

        :param label_index: the index of the data point you want to label.
        :param y: the data label.
        :return: None
        """
        if label_index < self.size:
            self.labels[label_index] = y
            self.labeled_ids.update([label_index])
        else:
            raise ValueError("make sure the given index is available")

    def label(self, x, y):
        """
        Label the single data by querying the data object itself.

        :param x: The data object you want to label.
        :param y: the data label.
        :return: None
        """
        if x in self.data:
            self.labels[np.where(self.data == x)] = y
        else:
            self.data = np.append(self.data, x)
            self.labels = np.append(self.labels, y)
            self.size += + 1
        self.labeled_ids.update(np.where(self.data == x)[0].tolist())

    def get_labeled_data(self):
        """
        Get all the labeled data objects, including the data and corresponding labels.
        :return: data, labels.
        """
        filter_ids = list(self.labeled_ids)
        return self.data[filter_ids], self.labels[filter_ids]

    def get_dataloader(self, data_x, data_y, batch_size, num_worker=1):
        """
        For PyTorch: get the data loader by calling the given dataset class.

        :param data_x: the data.
        :param data_y: the corresponding data labels.
        :param batch_size: the batch size for training/testing.
        :param num_worker: the number of workers to process the data.
        :return: A DataLoader object of PyTorch.
        """
        return DataLoader(TorchDataset(data_x, data_y),
                          shuffle=True,
                          batch_size=batch_size,
                          num_workers=num_worker)

    def get_train_loader(self, batch_size, num_worker=1):
        """
        For PyTorch: get the data loader using all the labeled data in the pool.
        :param batch_size: the batch size for training/testing.
        :param num_worker: the number of workers to process the data.
        :return: A DataLoader object of PyTorch.
        """
        return self.get_dataloader(*self.get_labeled_data(), batch_size, num_worker=num_worker)
