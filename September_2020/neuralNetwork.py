'''Make your own Neural Network
adapted from Tariq Rashid
May 30, 2017'''

import numpy as np
import random
#import matplotlib.pyplot as plt
from math import exp
#import scipy.special

class NeuralNetwork(object):

    #initialize the neural network
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        #link weight matrices, wih and who
        #weights inside the arrays are w_i_j, where link
        #is from node i to node j in the next layer
        #w11 w21
        #w12 w22 etc
        self.wih = np.random.normal(0.0, pow(self.hnodes, -0.5),
                                       (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, pow(self.onodes, -0.5),
                                       (self.onodes, self.hnodes))
        #self.net = [self.wih,self.who]
        #learning rate
        self.lr = learningrate
        pass

    def activation_function(self, x, sigm=True):
        #activation function is the sigmoid function
        '''for i,element in enumerate(x):
            #print("element: ",element)
            if sigm:
                out[i] = sigmoid(x[i][0])
            else:
                out[i] = relu(x[i][0])
            #print(out)'''
        # this can be done much faster using numpy
        out = sigmoid(x[:,0]) if sigm else relu(x[:,0]) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#
        return out.reshape(-1, 1) #NB this needs to be 2D so it can be used for output as well

    def replicate(self):
        output = NeuralNetwork(self.inodes, self.hnodes, self.onodes, self.lr)
        output.wih = np.copy(self.wih)
        output.who = np.copy(self.who)
        output.lr = self.lr
        return output

    def mutate(self, rate=0.3, amount=0.1):
        flat_wih = self.wih.flatten()
        for i,n in enumerate(flat_wih):
            if random.random() < rate:
                flat_wih[i] *= 1.0 + np.random.normal(0.0, amount)
        self.wih = np.copy(flat_wih.reshape(self.hnodes,self.inodes))

        flat_who = self.who.flatten()
        for i, n in enumerate(flat_who):
            if random.random() < rate:
                flat_who[i] *= 1.0 + np.random.normal(0.0, amount)
        self.who = np.copy(flat_who.reshape(self.onodes, self.hnodes))
        return self

    #train the neural network
    def train(self, inputs_list, targets_list):
        #convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        #calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        #calculate the signals emerging from hidden layer
        hidden_outputs = self.activation_function(hidden_inputs, False)

        #calculate signals entering final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        #calculate signals exiting final output layer
        final_outputs = self.activation_function(final_inputs, False)

        #output layer error is the (target - actual)
        output_errors = targets - final_outputs
        #hidden layer error is the output_errors, split by weights,
        #recombined at hidden nodes
        hidden_errors = np.dot(self.who.T, output_errors)

        #update the weights for the links between the
        #hidden and output layers
        self.who += self.lr * np.dot((output_errors * final_outputs *\
                                      (1.0 - final_outputs)),
                                     np.transpose(hidden_outputs))

        #update the weights for the links between the input
        #and hidden layers
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs *\
                                      (1.0 - hidden_outputs)),
                                     np.transpose(inputs))
        pass

    #query the neural network
    def query(self, inputs_list):
        #convert inputs list to 2d array
        inputs = np.array(inputs_list,ndmin=2).T

        #calculate signals into hidden layer
        hidden_inputs = np.dot(self.wih, inputs)
        #calculate the signals emerging from the
        #hidden layer
        #print("Hidden inputs:", hidden_inputs)
        hidden_outputs = self.activation_function(hidden_inputs, False)

        #calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        #calculate the signals emerging from final
        #output layer
        final_outputs = self.activation_function(final_inputs, False)
        #print("final_outputs: ",final_outputs)
        return final_outputs

def sigmoid(x):
    return 1.0 /(1.0 + np.exp(x * -1.0)) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#

def relu(x):
    return np.maximum(x, 0.0) #<><><><><><>#.#<><><><><><>#.#<><><><><><>#

def main():
    #number of input, hidden and output nodes
    input_nodes = 784
    hidden_nodes = 100
    output_nodes = 10

    #learning rate
    learning_rate = 0.3

    #create instance of neural network
    n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    #load the mnist training data CSV file into a list
    training_data_file = open('mnist_train_100.csv','r')
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    #train the neural network
    #go through all records in training data set
    for record in training_data_list:
        #split the record by the commas
        all_values = record.split(',')
        #scale and shift the inputs
        inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        #create the target output values (all 0.01 except the
        #desired label which is 0.99)
        targets = np.zeros(output_nodes) + 0.01
        #print("all values[0]: ",all_values[0])
        #print("targets: ",targets)
        #all values[0] is the target label for this record
        targets[int(all_values[0])] = 0.99
        n.train(inputs,targets)
        pass

    #load the mnist data csv file into a list
    test_data_file = open('mnist_test_10.csv','r')
    test_data_list = test_data_file.readlines()
    test_data_file.close()

    ###TO TEST###
    #get the first test record
    all_values = test_data_list[0].split(',')
    #print the label
    print(all_values[0])
    image_array = np.asfarray(all_values[1:]).reshape((28,28))
    plt.imshow(image_array, cmap="Greys", interpolation='None')
    plt.show()

    print(n.query((np.asfarray(all_values[1:]) / 255 * 0.99) + 0.01))

    '''a = np.zeros([3,2])
    a[0,0] = 1
    a[0,1] = 2
    a[1,0] = 9
    a[2,1] = 12
    
    plt.imshow(a, interpolation = 'nearest')
    plt.show()'''

    #print(n.query([1.0, 0.5, -1.5]))


def test():
    brain = NeuralNetwork(2, 3, 1, 0.8)
    print("brain:",brain.wih)
    brain2 = brain.replicate()
    print('brain2:',brain2.wih)
    brain2.mutate()
    print("brain2 mutated:", brain2.wih)
    # a = np.random.normal(0.0, pow(3, -0.5),
    #                                    (3,2))
    # print(a)
    #
    # a *= np.random.random()
    # print(a)
    # b = np.copy(a)
    # print(b)

if __name__ == "__main__":
    main()