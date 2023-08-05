import numpy as np
import sys, os
sys.path.append(os.path.abspath('./'))
from DFW.preprocess import *

config = {
    'database': {
        'name': 'AgeDB',
        'format': 'done_{name}_36x36_BIF_[L2_zscore]_D200_Age',
        'range': [16, 62],
        'labeled': True,
        'root': './data',
    },
    'process': {
        'center': True,
        'extend': True,
        'train': (5, 10, 15, 20, 25),
    }
}


def test_train_data(config = config):
    prepare, name = PreProcessTransfer(config), config['database']['name']
    assert isinstance(prepare, PreProcessTransfer)

    train, train_y, test, test_y = prepare.generator(config['process']['train'][-1], name, np.random.randint(0, 10))
    assert train.shape[-1] == train_y.shape[-1]
    assert test.shape[-1] == test_y.shape[-1]

    assert np.unique(train_y).size == config['database']['range'][-1] - config['database']['range'][0] + 1
    assert prepare.get_class_num(name) == config['database']['range'][-1] - config['database']['range'][0] + 1


def test_cv_train(config = config):
    prepare, name = PreProcessTransfer(config), config['database']['name']
    assert isinstance(prepare, PreProcessTransfer)

    group = prepare.generator(config['process']['train'][-1], name, np.random.randint(0, 10))
    train_num = group[0].shape[-1]

    for cv in range(prepare.get_cv(name)):
        cv_group = prepare.get_cv_data(cv)
        assert cv_group['train'].shape[-1] + cv_group['test'].shape[-1] == train_num


def test_cv5(config = config):
    config['process']['cv'] = 5
    prepare, name = PreProcessTransfer(config), config['database']['name']
    assert isinstance(prepare, PreProcessTransfer)

    _ = prepare.generator(config['process']['train'][-1], name, np.random.randint(0, 10))
    assert prepare.get_cv(name) == 5


def test_cv10(config = config):
    config['process']['cv'] = 10
    prepare, name = PreProcessTransfer(config), config['database']['name']
    assert isinstance(prepare, PreProcessTransfer)

    _ = prepare.generator(config['process']['train'][-1], name, np.random.randint(0, 10))
    assert prepare.get_cv(name) == 10


if __name__ == '__main__':
    test_cv_train(config)
    test_cv5(config)
    test_cv10(config)
    test_train_data(config)
