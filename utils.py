import os
from datetime import datetime

import numpy as np
import tensorflow as tf

from operator import itemgetter


class ReplayMemory:
    """
    Replay memory class to remember the actions taken by the agent
    Credits goes to https://github.com/ageron/handson-ml/blob/master/16_reinforcement_learning.ipynb
    """
    def __init__(self, maxlen):
        self.maxlen = maxlen
        self.buf = np.empty(shape=maxlen, dtype=np.object)
        self.index = 0
        self.length = 0

    def append(self, data):
        self.buf[self.index] = data
        self.length = min(self.length + 1, self.maxlen)
        self.index = (self.index + 1) % self.maxlen

    def sample(self, batch_size, with_replacement=True):
        if (self.length == 0):
            return None
        if with_replacement:
            indices = np.random.randint(self.length, size=batch_size)  # faster
        else:
            indices = np.random.permutation(self.length)[:batch_size]
        return self.buf[indices]

class GameReplayMemory:
    """
    Replay memory class to remember the actions taken by the agent
    Credits goes to https://github.com/ageron/handson-ml/blob/master/16_reinforcement_learning.ipynb
    """
    def __init__(self):
        self.buf = []
        self.length = 0

    def append(self, data):
        self.buf.append(data)
        self.length = self.length + 1

    def reset(self):
        self.buf = []
        self.length = 0

    def sample(self, batch_size, with_replacement=True):
        if (batch_size == 0):
            return None

        if (self.length == 0):
            return None

        if with_replacement:
            indices = np.random.randint(self.length, size=batch_size)  # faster
        else:
            indices = np.random.permutation(self.length)[:batch_size]

        if (len(indices) == 1):
            return [itemgetter(*indices)(self.buf)]

        return itemgetter(*indices)(self.buf)


def get_file_writer(model_name, session):
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    root_logdir = 'tf_logs/{}'.format(model_name)
    if not os.path.isdir(root_logdir):
        os.makedirs(root_logdir)

    log_dir = '{}/run-{}/'.format(root_logdir, now)
    file_writer = tf.compat.v1.summary.FileWriter(log_dir, session.graph)
    return file_writer


def get_checkpoint_path(model_name):
    model_path = './models/{}/'.format(model_name)

    if not os.path.isdir(model_path):
        os.makedirs(model_path)
    checkpoint_path = model_path + 'dqn.ckpt'
    return checkpoint_path
