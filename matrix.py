"""DIY Matrix Operations
Sept. 26, 2019"""

import random

class Matrix(object):
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        for r in range(self.rows):
            self.data.append([])
            for c in range(self.cols):
                self.data[r].append(0)

    def randomize(self):
        """Assigns random value between 0 and 1"""
        for r, row in enumerate(self.data):
            for i in range(self.cols):
                self.data[r][i] = random.random()

    def fromArray(self, arr):
        m = Matrix(len(arr),1)
        for i,val in enumerate(arr):
            m.data[i][0] = val
        return m

    def add(self,other):
        """Add a matrix to self"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] += other.data[i][j]

    def transpose(self):
        '''Transposes matrix'''

        output = []
        m = self.rows
        n = self.cols
        # create an n x m matrix
        for i in range(n):
            output.append([])
        for j in range(m):
        # replace a[i][j] with a[j][i]
            output[i].append(self.data[j][i])
        return output


    def multiply(self,b):
        '''Returns the product of
        matrix a and matrix b'''

        newmatrix = []
        for i in range(self.rows):
            row = []
            #for every column in b
            for j in range(b.cols):
                sum1 = 0
                #for every element in the column
                for k in range(b.rows):
                    sum1 += self.data[i][k]*b.data[k][j]
                row.append(sum1)
            newmatrix.append(row)
        self.data = newmatrix

    def multiply_scalar(self,b):
        """Returns self's data multiplied by
        a number b."""
        newmatrix = []
        for i in range(self.rows):
            row = [b * self.data[i][j] for j in range(self.cols)]
            newmatrix.append(row)

        self.data = newmatrix

    def map(self,func):
        """Returns self's data with a function applied."""
        newmatrix = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(func(self.data[i][j]))
            newmatrix.append(row)

        self.data = newmatrix

    def print_matrix(self):
        for row in self.data:
            print(row)


def g(x):
    return 2*x + 5
m2 = Matrix(2,2)
m3 = Matrix(2,2)
#m2.randomize()
m2 = 5
m3.randomize()
#print(type(m2))
#m2.data = [[1,2],[3,4]]
m3.data = [[5,6],[-2,-1]]
#print(m2.data)
#print(m3.data)
m3.map(g)
m3.print_matrix()
