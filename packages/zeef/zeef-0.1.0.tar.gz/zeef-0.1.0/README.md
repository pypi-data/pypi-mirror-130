# Zeef: Active Learning for Data-Centric AI

[![build](https://github.com/MLSysOps/zeef/actions/workflows/main.yml/badge.svg)](https://github.com/MLSysOps/zeef/actions/workflows/main.yml) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMLSysOps%2Fdeepal.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMLSysOps%2Fdeepal?ref=badge_shield)

Zeef is an active learning framework that can be applied to deep learning scenarios leak of labeled data. It contains many built-in data selection algorithms to reduce the labor of data annotation.


## Installation 

```shell
pip install zeef
```

For the local development, you can install from the [Anaconda](https://www.anaconda.com/) environment by 

```shell
conda env create -f environment.yml
```

A quick MNIST CNN example can be found in [here](./examples/main.py). Run 

```shell
conda activate zeef
python main.py
```

to start the quick demonstration. 

## Quick Start

We can start from the most easy example: random select data points from an unlabeled data pool.

```python
from zeef.data import Pool
from zeef.strategy import RandomSampling

# define the pool and active learning strategy. 
pool = Pool(torch_dataset_class, unlabeled_data)
strategy = RandomSampling(pool, network)

# start the active learning.
data_ids = strategy.query(1000)
# label those 1k sampled data points.
pool.label_by_ids(data_ids, data_labels) 
# retrain the model
strategy.learn()
# test the model
predictions = strategy.predict(test_x, test_y)
```

## License

[Apache License 2.0](./LICENSE)
