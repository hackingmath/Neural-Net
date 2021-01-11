import torch
import torch.nn as nn
import numpy as np
import random

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# Fully connected neural network with one hidden layer
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        super(NeuralNet, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden1_size)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(hidden1_size, hidden2_size)
        self.l3 = nn.Linear(hidden2_size, output_size)

    def forward(self, x):
        # x = x.double()
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        # no activation and no softmax at the end
        return out#astype(numpy.double)

    def mutate(self, rate=0.5, amount=0.1):
        for param in self.parameters():
            for i in range(param.shape[0]):
                if random.random() < rate:
                    param[i] += 1.0 + np.random.normal(0.0, amount)
        return self

model = NeuralNet(3,5,5,2)
print(model.state_dict())
model.mutate()
print(model.state_dict())
