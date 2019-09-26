"""DIY Neural Net
Sept. 26, 2019"""

import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def dsigmoid(y):
    return y * (1 - y)


class NeuralNetwork(object):
    def __init__(self, input_nodes,hidden_nodes,output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.weights_ih = Matrix(self.hidden_nodes,self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes,self.hidden_nodes)
        self.weights_ih.randomize()