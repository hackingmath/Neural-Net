"""DIY Matrix Operations
Sept. 26, 2019"""

import random

class Matrix(object):
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        for i in range(self.rows):
            self.data.append([])
            for j in range(self.cols):
                self.data[i].append(0)
                
    def __add__(self,B):
        """Add A matrix to B"""
        newmatrix = Matrix(self.rows,self.cols)
        newmatrix.data = []
        for i in range(self.rows):
            newmatrix.data.append([])
            for j in range(self.cols):
                newmatrix.data[i].append(self.data[i][j] + B.data[i][j])
        return newmatrix

    def __mul__(self,B):
        '''Returns the product of the corresponding
        terms of matrix a and matrix b'''

        newmatrix = Matrix(self.rows,self.cols)
        for i,row in enumerate(newmatrix.data):
            for j,col in enumerate(row):
                newmatrix.data[i][j] = self.data[i][j]*B.data[i][j]
        return newmatrix     

    def randomize(self):
        """Assigns random value between 0 and 1"""
        for r in range(self.rows):
            for i in range(self.cols):
                try:
                    self.data[r][i] = random.random()
                except:
                    pass#print(r,i,self.data)

    def copy(self):
        m = Matrix(self.rows,self.cols)
        for i, row in range(self.rows):
            for j in range(self.cols):
                m.data[i][j] = self.data[i][j]
        return m

    def transpose(self):
        '''Transposes matrix'''
    
        m = self.rows
        n = self.cols
        output = Matrix(n,m)
        #print(output.data)
        # create an n x m matrix
        for i in range(n):
            for j in range(m):
                if m > 1:
                    # replace a[i][j] with a[j][i]
                    output.data[i][j] = self.data[j][i]
                else:
                    output.data[i] = self.data[j]
        return output

    def multiply_scalar(self,b):
        """Returns self's data multiplied by
        a number b."""
        newdata = []
        for i in range(self.rows):
            row = [b * self.data[i][j] for j in range(self.cols)]
            newdata.append(row)
        self.data = newdata[::]
        return self

    def dot(self,B):
        '''Returns the product of
        matrix a and matrix b'''
        newmatrix = Matrix(self.rows,B.cols)
        newmatrix.data = []
        for i in range(self.rows):
            
            newmatrix.data.append([])
            #for every column in b
            for j in range(B.cols):
                sum1 = 0
                #for every element in the column
                for k in range(B.rows):
                    if B.cols > 1:
                        sum1 += self.data[i][k]*B.data[k][j]
                    else:
                        sum1 += self.data[i][k]*B.data[k]

                newmatrix.data[i].append(sum1)
        return newmatrix


def fromArray(arr):
    m = Matrix(len(arr),1)
    for i,val in enumerate(arr):
        m.data[i][0] = val
    return m

def transposeOLD(A):
    '''Transposes matrix'''

    output = []
    m = len(A)
    n = len(A[0])
    # create an n x m matrix
    for i in range(n):
        output.append([])
    for j in range(m):
    # replace a[i][j] with a[j][i]
        output[i].append(A[j][i])
    return output


def map(A,func):
    """Returns self's data with a function applied."""
    newmatrix = []
    for i in range(A):
        row = []
        for j in range(len(A[0])):
            row.append(func(A[i][j]))
        newmatrix.append(row)

    return newmatrix

def print_matrix(A):
    for row in A:
        print(row)


def g(x):
    return 2*x + 5


if __name__ == '__main__':
    m2 = Matrix(1,5)
    m3 = Matrix(5,4)
    #m2.randomize()
    #print(m2.data)
    #m2 = 5
    #m3.randomize()
    #print(type(m2))
    m2.data = [[1,-2,3,4,-5]]
    m3.data = [[1,2,0,3],[0,4,-1,5],[6,0,4,-2],[2,-1,-3,0],[1,-2,3,0]]
    #print(m2.data)
    #print(m3.data)
    #print(dot(m2,m3).data)
    print(m2.dot(m3).data)
