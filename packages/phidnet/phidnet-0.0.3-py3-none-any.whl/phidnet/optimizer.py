import numpy as np
import random

from phidnet import network_data



class SGD:   # SGD optimizer
    def __init__(self, lr=0.01):
        self.lr = lr

    def update(self):
        for i in range(network_data.layerNumber, 0, -1):  # i: 3, 2, 1...  Update weights and biases with their gradients
            network_data.weight[i] -= self.lr * network_data.deltaWeight[i]
            network_data.bias[i] -= self.lr * network_data.deltaBias[i]



class Momentum:   # Momentum optimizer
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.weight_v = None
        self.bias_v = None

    def update(self):

        if self.weight_v is None:
            self.weight_v = {}
            for i in range(1, network_data.layerNumber + 1):
                self.weight_v[i] = np.zeros_like(network_data.weight[i]) + random.random()

        if self.bias_v is None:
            self.bias_v = {}
            for i in range(1, network_data.layerNumber + 1):
                self.bias_v[i] = np.zeros_like(network_data.bias[i]) + random.random()

        for i in range(network_data.layerNumber, 0, -1):  # i: 3, 2, 1...  Update weights and biases with their gradients
            self.weight_v[i] = self.momentum * self.weight_v[i] - self.lr * network_data.deltaWeight[i]
            self.bias_v[i] = self.momentum * self.bias_v[i] - self.lr * network_data.deltaBias[i]
            network_data.weight[i] += self.weight_v[i]
            network_data.bias[i] += self.bias_v[i]