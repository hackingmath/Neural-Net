'''From Siraj's Video
https://www.youtube.com/watch?v=h3l4qz76JhQ
April 7, 2019
'''

import numpy as np

def nonLin(x,deriv = False):
    '''The Sigmoid Activation Function?'''
    if deriv == True:
        return x*(1-x)
    return 1/(1+np.exp(-x))

#input data
X = np.array([[0,0,1],
              [0,1,1],
              [1,0,1],
              [1,1,1]])

#output data
y = np.array([[0],
              [1],
              [1],
              [0]])

np.random.seed(1)

#synapses
syn0 = 2*np.random.random((3,4)) - 1
syn1 = 2*np.random.random((4,1)) - 1

#training step
for j in range(60000):
    l0 = X
    l1 = nonLin(np.dot(l0,syn0))
    l2 = nonLin(np.dot(l1,syn1))

    l2_error = y - l2

    if j % 10000 == 0:
    # print("l1:",l1)
    # print("l2:",l2)
        print("Error:",np.mean(np.abs(l2_error)))

    l2_delta = l2_error*nonLin(l2,True)

    l1_error = l2_delta.dot(syn1.T)

    l1_delta = l1_error * nonLin(l1,True)


    #update weights
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)

    # print("l2_delta:",l2_delta)
    # print("l1_error:",l1_error)
    # print("l2_error:",l2_error)
    # print('l1_delta:',l1_delta)
    # print("syn1:",syn1)
    # print("syn0:",syn0)
    #
    # print('*******')
    # print("Loop #",j)
    # print()

print("Output after training")
print(l2)