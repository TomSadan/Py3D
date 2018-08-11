import pygame, inspect
from math import sin, cos, tan, radians
from Matrix import *
from Exceptions import *


# Constants
X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2

ORIGIN = 0

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
BROWN     = (200, 80, 0)
WHITE     = (255,255,255)


# Classes
class Container(object):
    def __init__(self):
        self._items = []
		
    def push(self, item):
        self._items.append(item)
		
    def isEmpty(self):
        return len(self._items) == 0
	
	
class Stack(Container):
    def pop(self):
        return self._items.pop()
		
		
class Queue(Container):
    def pop(self):
        return self._items.pop(0)
	
# TODO: Implement VectorUtils class to work with the Vector class
class VectorUtils(object):
    @staticmethod
    def getDirectionVector(coord1, coord2):
        slope = []
        for dim in range(VectorUtils.dimensionOf(coord1)):
            slope.append(coord2[dim]-coord1[dim])
        return list(slope)

    @staticmethod
    def getUnitVector(vector):
        magnitude = VectorUtils.getMagnitude(vector)
        unitVector = VectorUtils.multiplyByScalar(vector, 1/float(magnitude))
        return unitVector

    @staticmethod
    def getSlopeInt(coord1, coord2):
        if not (VectorUtils.dimensionOf(coord1) == dimensionOf(coord2) == 2):
            raise IncorrectDimensionException()
        distanceVector = getDirectionVector(coord1, coord2)
        return distanceVector[X_INDEX]/float(distanceVector[Y_INDEX])

    @staticmethod
    def getSlopeVector(coord1, coord2):
        return getUnitVector(getDirectionVector(coord1, coord2))

    @staticmethod
    def getMagnitude(vector):
        magnitude = 0
        for dim in range(VectorUtils.dimensionOf(vector)):
            magnitude += vector[dim]**2
        magnitude = math.sqrt(magnitude)
        return magnitude

    @staticmethod
    def dimensionOf(vector):
        return len(vector)

    @staticmethod  
    def addVectors(vector1, vector2):
        resultantVector = []
        for dim in range(VectorUtils.dimensionOf(vector1)):
            resultantVector.append(vector1[dim] + vector2[dim])
        return resultantVector

    @staticmethod
    def subtractVectors(vector1, vector2):
        return VectorUtils.addVectors(vector1, VectorUtils.multiplyByScalar(vector2, -1))

    @staticmethod
    def multiplyByScalar(vector, scalar):
        resultantVector = []
        for dim in range(VectorUtils.dimensionOf(vector)):
            resultantVector.append(scalar * vector[dim])
        return resultantVector
    
# TODO: Make classes for 3D shapes and implement them

class Background(object):
    def __init__(self, colour):
        self._colour = colour

    def draw(self, py3d):
        py3d.getSurface().fill(self._colour)


class Pixel(object):
    def __init__(self, colour, x, y, z):
        self._pos = [x,y,z]
        self._colour = colour

    def draw(self, py3d):
        # TODO: Optimize the calls for mapCoordinates so they aren't being called unecessarily (DO THIS FOR ALL SHAPE OBJECTS THAT CALL IT)
        py3d.getSurface().fill(self._colour, (py3d.mapCoordinates(self._pos[X_INDEX], self._pos[Y_INDEX], self._pos[Z_INDEX]), (3, 3)))


class Line(object):
    def __init__(self, colour, start_pos, end_pos):
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._colour = colour

    def draw(self, py3d):
        # TODO: Optimize the calls for mapCoordinates so they aren't being called unecessarily (DO THIS FOR ALL SHAPE OBJECTS THAT CALL IT)
         pygame.draw.line(py3d.getSurface(), self._colour,
                          py3d.mapCoordinates(self._start_pos[X_INDEX], self._start_pos[Y_INDEX], self._start_pos[Z_INDEX]),
                          py3d.mapCoordinates(self._end_pos[X_INDEX], self._end_pos[Y_INDEX], self._end_pos[Z_INDEX]), 2)


class Polyhedron(object):
    def __init__(self, coordinates, width=0):
        self._coords = coordinates
        self._width = width

    def draw(self, py3d):
        for dot_pos in self._coords:
            py3d.fill(RED, dot_pos[X_INDEX], dot_pos[Y_INDEX], dot_pos[Z_INDEX])

        if self._width == 0:
            #TODO: DONT DO THIS FOR THE LOVE OF GOD IM HIGH
            squareSides = [ [self._coords[0]] + [self._coords[1]] + [self._coords[3]] + [self._coords[2]],
                           [self._coords[0]] + [self._coords[1]] + [self._coords[5]] + [self._coords[4]],
                           [self._coords[0]] + [self._coords[4]] + [self._coords[6]] + [self._coords[2]],
                           [self._coords[2]] + [self._coords[6]] + [self._coords[7]] + [self._coords[3]],
                           [self._coords[4]] + [self._coords[6]] + [self._coords[7]] + [self._coords[5]],
                           [self._coords[1]] + [self._coords[5]] + [self._coords[7]] + [self._coords[3]] ]
            for squareSide in squareSides:
                convertedCoords = [py3d.mapCoordinates(pos[X_INDEX], pos[Y_INDEX], pos[Z_INDEX]) for pos in squareSide]
                pygame.draw.polygon(py3d.getSurface(), GREEN, convertedCoords, 0)
##                pygame.draw.lines(py3d.getSurface(), BLUE, False, convertedCoords, 7)
        for start_pt in self._coords:
            clone = list(self._coords)
            clone.remove(start_pt)
            for end_pt in clone:     
                py3d.drawLine(BLUE, start_pt, end_pt)  

class Rectangle(Polyhedron): #TODO: IMPLEMENT THIS
    def __init__(self, colour, pos, width, height): # TODO: Think of nicer variable names
        self._colour = colour #TODO: JUST KEEP SELF._COLOUR AND USE SELF._COORDS
        self._pos = pos
        self._width = width
        self._height = height

    def draw(self, py3d):
        pass
        #pygame.draw.rect(py3d.getSurface(), self._colour, (py3d.mapCoordinates(self.pos[X_INDEX], self.pos[Y_INDEX], self.pos[Z_INDEX]), width, height), 1)


class Square(Rectangle):
    def __init__(self, pos, side_length):
        super(Square, self).__init__(pos, side_length, side_length)

    
class Parallelepiped(Polyhedron):
    pass # TODO: Implement this class

        
class Py3D(object):
    def __init__(self, size, origin, vanishOffset):
        self._origin = origin
        self._vanishOffset = vanishOffset
        self._mult = 0.001

        self._drawingQueue = Queue()

        pygame.init()

        self._clock = pygame.time.Clock()

        self._SIZE = size

        self._surface = pygame.display.set_mode(self._SIZE)
        pygame.display.set_caption("Py3D Demo")
        font = pygame.font.Font(None, 24) 

    def mapCoordinates(self, x, y, z):
        distanceVector = VectorUtils.getDirectionVector((x, y), self._vanishOffset)
        scalarFunc = 1+(-1/float((self._mult*z+1))) # Domain of z: [0, inf)
        z_axisOffsetVector = VectorUtils.multiplyByScalar(distanceVector, scalarFunc)
        absoluteVector = VectorUtils.addVectors((x,y), z_axisOffsetVector)
        resultantVector = VectorUtils.addVectors(self._origin, [absoluteVector[X_INDEX], -absoluteVector[Y_INDEX]])
        return resultantVector

    def getSurface(self):
        return self._surface
    
    def clear(self):
        self._drawingQueue = Queue()
		
    def draw(self):
        while not self._drawingQueue.isEmpty():
            drawObject = self._drawingQueue.pop()
            drawObject.draw(self)
        pygame.draw.line(self._surface, BLUE, self._origin, VectorUtils.addVectors(self._origin, [self._vanishOffset[X_INDEX], -self._vanishOffset[Y_INDEX]]), 3)
        pygame.draw.line(self._surface, BLUE, self._origin, VectorUtils.addVectors(self._origin, [1000, 0]), 3)
        pygame.draw.line(self._surface, BLUE, self._origin, VectorUtils.subtractVectors(self._origin, [0, 1000]), 3)
        self._surface.fill(RED, (self._origin, (1, 1)))
        self._surface.fill(GREEN, (VectorUtils.addVectors(self._origin, self._vanishOffset), (1, 1)))
        pygame.display.update()

    def fill(self, colour, x=None, y=None, z=None):
        if x is None or y is None or z is None:
            self.pushToQueue(Background(colour))
        else:
            self.pushToQueue(Pixel(colour, x, y, z))

    def drawLine(self, colour, start_pos, end_pos):
        self.pushToQueue(Line(colour, start_pos, end_pos))

    def pushToQueue(self, item):
        # If item has an attribute called "draw"
        # And this attribute is a method
        # And this method has 2 parameters
        # Then the item is a valid Queue item
        drawMethod = getattr(item, "draw", None)
        if drawMethod == None or not callable(drawMethod) or len(inspect.getargspec(drawMethod)[0]) != 2:
            raise AttributeError("Queue item must have the following method signature: draw(self, py3d)")
        self._drawingQueue.push(item)

    def rotateCoordinates(self, pos, axisOfRotation, origin, theta):
        xRotMatrix = Matrix([ [1, 0, 0],
                              [0, cos(radians(theta)), -sin(radians(theta))],
                              [0, sin(radians(theta)), cos(radians(theta))] ])
        
        yRotMatrix = Matrix([ [cos(radians(theta)), 0, sin(radians(theta))],
                              [0, 1, 0],
                              [-sin(radians(theta)), 0, cos(radians(theta))] ])
        
        zRotMatrix = Matrix([ [cos(radians(theta)), -sin(radians(theta)), 0],
                              [sin(radians(theta)), cos(radians(theta)), 0],
                              [0, 0, 1] ])
        # 1) Find direction vector from origin to pos
        directionVector = VectorUtils.getDirectionVector(origin, pos)
        #print "directionVector: " + str(directionVector)
        # 2) Perform a rotation of direction vector theta degrees about origin in respect to axisOfRotation
        # Logic is {axisOfRotation}RotMatrix * columnVector of direction vector
        switcher = {
                X_INDEX: xRotMatrix,
                Y_INDEX: yRotMatrix,
                Z_INDEX: zRotMatrix
        }
        rotationMatrix = switcher[axisOfRotation]
        columnVector = Vector(directionVector).transpose()
        #print "rotationMatrix:\n" + str(rotationMatrix) + "\n" + "columnVector:\n" + str(columnVector)
        newDirectionVector = rotationMatrix * columnVector
        #print "newDirectionVector: \n" + str(newDirectionVector)
        

        # 3) Add the the result from 2 to origin
        return VectorUtils.addVectors(origin, newDirectionVector.transpose()._contents[0]) #TODO: Change this and use vector / matrix methods
        

if (__name__ == "__main__"):
    def addValue(coordList, dim, value):
        for coord in coordList:
            coord[dim] += value

    def getCubeCenter():
        global cube_pts
        a = cube_pts[0]
        b = cube_pts[1]
        c = cube_pts[2]
        d = cube_pts[4]
        ab = VectorUtils.getDirectionVector(a,b)
        ac = VectorUtils.getDirectionVector(a,c)
        ad = VectorUtils.getDirectionVector(a,d)
        cubeCenter = VectorUtils.addVectors(a, VectorUtils.multiplyByScalar(VectorUtils.addVectors(ab, VectorUtils.addVectors(ac, ad)), 0.5))
        return cubeCenter

    speed = 5
    
    SCREEN_SIZE = (640, 480)
    gameEngine = Py3D(SCREEN_SIZE, [1, SCREEN_SIZE[Y_INDEX]-1], [SCREEN_SIZE[X_INDEX]//2, SCREEN_SIZE[Y_INDEX]//2])
    rect_pos = [0, 0, 0]
    rect_size = [300,300,300]
    cube_pts = [ [rect_pos[X_INDEX], rect_pos[Y_INDEX], rect_pos[Z_INDEX]],
                 [rect_pos[X_INDEX] + rect_size[X_INDEX], rect_pos[Y_INDEX], rect_pos[Z_INDEX]],
                 [rect_pos[X_INDEX], rect_pos[Y_INDEX] + rect_size[Y_INDEX], rect_pos[Z_INDEX]],
                 [rect_pos[X_INDEX] + rect_size[X_INDEX], rect_pos[Y_INDEX] + rect_size[Y_INDEX], rect_pos[Z_INDEX]],

                 [rect_pos[X_INDEX], rect_pos[Y_INDEX], rect_pos[Z_INDEX] + rect_size[Z_INDEX]],
                 [rect_pos[X_INDEX] + rect_size[X_INDEX], rect_pos[Y_INDEX], rect_pos[Z_INDEX] + rect_size[Z_INDEX]],
                 [rect_pos[X_INDEX], rect_pos[Y_INDEX] + rect_size[Y_INDEX], rect_pos[Z_INDEX] + rect_size[Z_INDEX]],
                 [rect_pos[X_INDEX] + rect_size[X_INDEX], rect_pos[Y_INDEX] + rect_size[Y_INDEX], rect_pos[Z_INDEX] + rect_size[Z_INDEX]] ]

    cubeCenter = getCubeCenter()

    run = True

    while run:
        pygame.event.get()
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_ESCAPE]:
            run = False
        
        if keys[pygame.K_RIGHT]:
            addValue(cube_pts, X_INDEX, speed)
                
        if keys[pygame.K_LEFT]:
            addValue(cube_pts, X_INDEX, -speed)

        if keys[pygame.K_UP]:
            addValue(cube_pts, Z_INDEX, speed)
                
        if keys[pygame.K_DOWN]:
            addValue(cube_pts, Z_INDEX, -speed)

        if keys[pygame.K_w]:
            addValue(cube_pts, Y_INDEX, speed)
                
        if keys[pygame.K_s]:
            addValue(cube_pts, Y_INDEX, -speed)

        if keys[pygame.K_j]:
            gameEngine._vanishOffset[X_INDEX] -= speed

        if keys[pygame.K_l]:
            gameEngine._vanishOffset[X_INDEX] += speed

        if keys[pygame.K_i]:
            gameEngine._vanishOffset[Y_INDEX] += speed

        if keys[pygame.K_k]:
            gameEngine._vanishOffset[Y_INDEX] -= speed

        if keys[pygame.K_m]:
            gameEngine._mult += 0.001

        if keys[pygame.K_n]:
            gameEngine._mult -= 0.001
            
        if keys[pygame.K_x]:
            for pt in range(len(cube_pts)):
                cube_pts[pt] = gameEngine.rotateCoordinates(cube_pts[pt], X_INDEX, cubeCenter, 3)

        if keys[pygame.K_y]:
            for pt in range(len(cube_pts)):
                cube_pts[pt] = gameEngine.rotateCoordinates(cube_pts[pt], Y_INDEX, cubeCenter, 3)

        if keys[pygame.K_z]:
            for pt in range(len(cube_pts)):
                cube_pts[pt] = gameEngine.rotateCoordinates(cube_pts[pt], Z_INDEX, cubeCenter, 3)
                    
        gameEngine.clear()
        gameEngine.fill(WHITE)
        gameEngine.pushToQueue(Polyhedron(cube_pts))
        gameEngine.draw()
        gameEngine._clock.tick(100)
    pygame.quit()
        
