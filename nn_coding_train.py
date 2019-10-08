"""DIY Neural Net
Adapted from Coding Train
https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_100.5_NeuroEvolution_FlappyBird/P5/neuralnetwork/nn.js
Sept. 26, 2019"""

import math
from matrix import Matrix
import random

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def dsigmoid(y):
    return y * (1 - y)

def tanh(x):
    return math.tanh(x)

def dtanh(y):
    return 1 - y**2

def relu(x):
    return max(0,x)

class NeuralNetwork(object):
    def __init__(self, input_nodes,hidden_nodes,output_nodes,
                 learningrate):
        self.input_nodes = input_nodes #int
        self.hidden_nodes = hidden_nodes #int
        self.output_nodes = output_nodes #int

        self.weights_ih = Matrix(self.hidden_nodes,self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes,self.hidden_nodes)
        self.weights_ih.randomize()
        self.weights_ho.randomize()

        self.bias_h = Matrix(self.hidden_nodes,1)
        self.bias_o = Matrix(self.output_nodes,1)
        self.bias_h.randomize()
        self.bias_o.randomize()

        self.lr = learningrate

    def copy(self):
        output = NeuralNetwork(self.input_nodes,self.hidden_nodes,self.output_nodes,
                               self.lr)
        output.weights_ih = self.weights_ih
        output.weights_ho = self.weights_ho
        output.bias_h = self.bias_h
        output.bias_o = self.bias_o

        return output

    def activation_function(self,x):
        """Applies the Sigmoid Function"""
        out = [0]*x.rows
        for i, element in enumerate(x.data):
            #print("element:",element)
            out[i] = sigmoid(x.data[i][0])
            #print(out)
        output = Matrix(1,x.rows)
        output.data = out[::]
        return output

    def activation_function_relu(self,x):
        """Applies the RELU function"""
        out = [0]*x.rows
        for i,element in enumerate(x.data):
            out[i] = relu(x.data[i][0])
        output = Matrix(1,x.rows)
        output.data = out[::]
        return output
    
    def mutate(self,rate):
        """bird's brain's weights mutate"""
        if random.random() < rate:
            offset = random.random()#*0.5
            rate += offset

        self.weights_ih.multiply_scalar(rate)
        self.weights_ho.multiply_scalar(rate)
        self.bias_h.multiply_scalar(rate)
        self.bias_o.multiply_scalar(rate)

    #train the neural network
    def train(self,inputs_list,targets_list):
        #convert inputs list to 2d array
        inputs = inputs_list.transpose()
        targets = targets_list.transpose()

        #calculate signals into hidden layer
        hidden_inputs = dot(self.weights_ih,inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        #calculate signals entering final output layer
        final_inputs = dot(self.weights_ho,hidden_outputs)
        #calculate signals exiting final output layer
        final_outputs = self.activation_function(final_inputs)

        #output layer error is the target - actual
        output_errors = targets - final_outputs
        #hidden layer error is the output_errors, split by weights,
        #recombined at hidden nodes
        hidden_errors = dot(transpose(self.weights_ho),output_errors)

        #update the weights for the links between the hidden and output layers
        hidden_step = multiply_element(output_errors,final_inputs)
        hidden_step.multiply_scalar(hidden.step,(1.0 - final_outputs))
        dot_hidden1 = dot(hidden_step, transpose(hidden_outputs))
        self.weights_ho += multiply_scalar(self.lr,dot_hidden1) 

        #update the weights for the links between the input and hidden layers
        hidden_step2 = multiply_element(hidden_errors,hidden_outputs)
        hidden_step2.multiply_scalar(hidden_step2,(1.0 - hidden_outputs))
        dot_hidden2 = dot(hidden_step2,transpose(inputs))
        self.weights_ih += multiply_scalar(self.lr,dot_hidden2) 

    def predict(self,inputs_list):
        #convert inputs list to 2d array
        inputs = Matrix(1,len(inputs_list))
        inputs.data = inputs_list
        #print("inputs:",inputs,type(inputs))
        #inputs.transpose()
        #targets = transpose(targets_list)

        #calculate signals into hidden layer
    
        hidden_inputs = self.weights_ih.dot(inputs.transpose())
        hidden_outputs = self.activation_function(hidden_inputs)

        #calculate signals entering final output layer
        #print("self.weights_ho:",self.weights_ho.rows,self.weights_ho.cols,
        #"hidden_outputs:",hidden_outputs.rows,hidden_outputs.cols)
        final_inputs = self.weights_ho.dot(hidden_outputs.transpose())
        #calculate signals exiting final output layer
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

def main():
    n = NeuralNetwork(5,8,2,0.3)
    ins = [1,2,3,4,5]
    #print(n.predict(ins))
    #from Tariq's book
    #Number of input, hidden, output nodes
    '''input_nodes = 784
    hidden_nodes = 100
    output_nodes = 10

    #learning rate
    learning_rate = 0.3

    #create instance of neural network
    n = NeuralNetwork(input_nodes,hidden_nodes,output_nodes,
                        learning_rate)
    training_data_file = open('mnist_train_100.csv','r')
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    #train the neural network
    #go through all the records in the training data set
    for record in training_data_list:
        #split the record by the commas
        all_values = record.split(',')
        #scale and shift the inputs
        inputs = multiply_scalar(1/255.0)
    '''

if __name__ == "__main__":
    main()