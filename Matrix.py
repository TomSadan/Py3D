from Exceptions import *

class Matrix(object):
    def __init__(self, contents):
        if isinstance(contents, Matrix):
            self._contents = contents._getItems()
        else:
            if not Matrix._validateContents(contents):
                raise IncorrectDimensionException("Not a valid Matrix.")
            self._contents = list(contents)
            
    @staticmethod
    def _validateContents(contents):
##        print contents
        for row in range(len(contents)-1):
            if len(contents[row]) != len(contents[row + 1]):
                return False
        return True

    def __applyMethod(self, other, method):
        if not isinstance(other, Matrix):
            raise TypeError("Other object should be a Matrix.")
        if len(self) != len(other):
            raise IncorrectDimensionException("Matrices must have the same number of rows and columns.")
        resultantItems = []
        for row in range(self.numRows()):
            resultantItems.append([])
            for col in range(self.numCols()):
                resultantItems[-1].append(method(self[row][col], other[row][col]))
        return Matrix(resultantItems)

    def _getItems(self):
        return list(self._contents)

    def __add__(self, other):
        return self.__applyMethod(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.__applyMethod(other, lambda a, b: a - b)

    def __mul__(self, other):
        if isinstance(other, (int, float, long)):
            return self.__applyMethod(Matrix([[other] * self.numCols()] * self.numRows()), lambda a, b: a * b)
        if isinstance(other, Matrix) == False:
            raise TypeError("Other object should be a Matrix.")
        if self.numCols() != other.numRows():
            raise IncorrectDimensionException("First Matrix must have number of rows equal to the number of columns in the second matrix.")
        resultantItems = []
        for self_row in self._contents: #TODO: Maybe don't access self._contents like that
            resultantItems.append([])
            for other_col in other.transpose():
                # DOT PRODUCT LOGIC
                resultantItems[-1].append(0)
                for i in range(self.numCols()):
                    resultantItems[-1][-1] += self_row[i] * other_col[i]
        return Matrix(resultantItems)

    def __pow__(self, other):
        if isinstance(other, int):
    	# TODO: Do the dot product with self "other" amount of times
            pass

    def __len__(self):
        return self.numRows() * self.numCols()
            
    def __getitem__(self, index):
        return self._contents[index]

    def __repr__(self):
        string = ""
        for row in self:
            string += "|"
            for col in row:
                string += " " + str(col)
            string += " |\n"
        return string

    def numRows(self):
        return len(self._contents)

    def numCols(self):
        return len(self._contents[0])

    def transpose(self):
        resultantItems = []
        for col_idx in range(self.numCols()):
            resultantItems.append([])
            for row in self._contents: #TODO: Maybe don't access self._contents like that
                resultantItems[-1].append(row[col_idx])
        return Matrix(resultantItems)
    

class Vector(Matrix):
    def __init__(self, *args):
##        print "args: " + str(args)
##        print "len args: " + str(len(args))
        if len(args) == 1:
            if isinstance(args[0], Matrix):
                super(Vector, self).__init__(args[0])
            elif isinstance(args[0], list):
                super(Vector, self).__init__([args[0]])
            else:
                raise TypeError("Vector.__init__ only accepts Matrix, list, or int *args.")
        else:
            super(Vector, self).__init__([args])

    def __getitem__(self, index):
        return self._contents[0][index]
    
    def __repr__(self):
        return Matrix(self).__repr__()

    def __pow__(self, other):
        if isinstance(other, int):
            super(Vector, self).__mul__(other)
        elif isinstance(other, Vector):
            # TODO: Do the cross product here
            pass
        else:
            raise TypeError("Vector must be raised to the power of an integer or another Vector.")

    def directionTo(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Other object should be a Vector.")
        if len(self) != len(other):
            raise IncorrectDimensionException("Other Vector should have the same dimension as this one.")
        slope = []
        for dim in range(len(self)):
            slope.append(other[dim]-self[dim])
        return Vector(slope)

    def unitVector(self):
        magnitude = len(self)
        unitVector = VectorUtils.multiplyByScalar(self, 1/float(magnitude))
        return unitVector

    def floatSlope(self, other):
        if not (VectorUtils.dimensionOf(coord1) == dimensionOf(coord2) == 2):
            raise IncorrectDimensionException()
        distanceVector = getDirectionVector(coord1, coord2)
        return distanceVector[X_INDEX]/float(distanceVector[Y_INDEX])

    def vectorSlope(self, other):
        return getUnitVector(getDirectionVector(coord1, coord2))

    def magnitude(self):
        magnitude = 0
        for dim in range(VectorUtils.dimensionOf(vector)):
            magnitude += vector[dim]**2
        magnitude = math.sqrt(magnitude)
        return magnitude

    @staticmethod
    def multiplyByScalar(vector, scalar):
        resultantVector = []
        for dim in range(VectorUtils.dimensionOf(vector)):
            resultantVector.append(scalar * vector[dim])
        return resultantVector


        
if (__name__ == "__main__"):
    myMatrix1 = Matrix([ [1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9] ])
    myMatrix2 = Matrix([ [0, -4, 2],
                         [7, 14, 2],
                         [1, 8, -20] ])

    print "Matrix 1\n" + str(myMatrix1) + " has " + str(len(myMatrix1)) + " items."
    print "Matrix 1's transpose is\n" + str(myMatrix1.transpose()) + " ."
    print "Matrix 2\n" + str(myMatrix2) + " has " + str(len(myMatrix2)) + " items."
    print "Matrix 2's transpose is\n" + str(myMatrix2.transpose()) + " ."
    print "Matrix 1 times Matrix 2 is\n" + str(myMatrix1 * myMatrix2) + " ."
    myVector1 = Vector(1,2,3,4)
    myVector2 = Vector(0,-2,7,4)
    print "Vector 1\n" +str(myVector1) + " has " + str(len(myVector1)) + " items."
    print "Vector 1's transpose is\n" + str(myVector1.transpose()) + " ."
    print "Vector 2\n" +str(myVector2) + " has " + str(len(myVector2)) + " items."
    print "Vector 2's transpose is\n" + str(myVector2.transpose()) + " ."
    print "Vector 1 times Vector 2's transpose is\n" + str(myVector1 * myVector2.transpose()) + " ."
    myVector1Copy = Vector(myVector1)
    print "I copied Vector 1, it is " + ("" if myVector1Copy is myVector1 else "not ") + "the same address as Vector 1, and its contents are: " + str(myVector1Copy)
    
    
