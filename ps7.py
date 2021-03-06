import math
import random

import ps7_visualize
import pylab

# For Python 2.7:
from ps7_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, comment out what's above and
# uncomment this line (for Python 2.6):
# from ps7_verify_movement26 import testRobotMovement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanedTiles = []   
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        p = int(pos.getX())
        q = int(pos.getY())
        if (p,q) not in self.cleanedTiles:
            self.cleanedTiles.append((p,q))
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        p = int(m)
        q = int(n)
        t = (p,q)
        if t in self.cleanedTiles:
            return True
        return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.height*self.width

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanedTiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        p = Position(int(random.random()*self.width),int(random.random()*self.height))
        return p
    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX();
        y = pos.getY();
        if cmp(x,0)==-1:
            return False
        elif cmp(y,0)==-1:
            return False
        x = int(x)
        y = int(y)
        if x in range(0,self.width):
            if y in range(0,self.height):
                return True
        return False

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.pos = self.room.getRandomPosition();
        self.direction = int(random.random()*360)
        self.room.cleanTileAtPosition(self.pos)
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!



# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newp = self.pos.getNewPosition(self.direction,self.speed)
        while(True):
            dec = self.room.isPositionInRoom(newp)
            if dec==True:
                x2 = int(newp.getX());
                y2 = int(newp.getY());
                x1 = int(self.pos.getX());
                y1 = int(self.pos.getY());
                for i in range(min(x1,x2),max(x1,x2)+1):
                    for j in range(min(y1,y2),max(y1,y2)+1):
                        p = (j*x2)-(j*x1)-(x2*y1)+(x1*y1)-(i*y2)+(x1*y2)+(i*y1)-(x1*y1)
                        if p==0:
                            if not(self.room.isTileCleaned(i,j)):
                                p = Position(i,j)
                                self.room.cleanTileAtPosition(p)
                self.setRobotPosition(newp)
                return
            else:
                self.setRobotDirection(int(random.random()*360))
                newp = self.room.getRandomPosition()

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newp = self.pos.getNewPosition(self.direction,self.speed)
        while(True):
            dec = self.room.isPositionInRoom(newp)
            if dec==True:
                x2 = int(newp.getX());
                y2 = int(newp.getY());
                x1 = int(self.pos.getX());
                y1 = int(self.pos.getY());
                for i in range(min(x1,x2),max(x1,x2)+1):
                    for j in range(min(y1,y2),max(y1,y2)+1):
                        p = (j*x2)-(j*x1)-(x2*y1)+(x1*y1)-(i*y2)+(x1*y2)+(i*y1)-(x1*y1)
                        if p==0:
                            if not(self.room.isTileCleaned(i,j)):
                                p = Position(i,j)
                                self.room.cleanTileAtPosition(p)
                self.setRobotPosition(newp)
                self.setRobotDirection(int(random.random()*360))
                return
            else:
                self.setRobotDirection(int(random.random()*360))
                newp = self.room.getRandomPosition()
# Uncomment this line to see your implementation of StandardRobot in action!



def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    tr = []
    bots = []
    room = RectangularRoom(width,height)
    size = (room.getNumTiles()*min_coverage)
    for i in range(num_robots):
        bots.append(robot_type(room,speed))
    for i in range(num_trials):
        anim = ps7_visualize.RobotVisualization(num_robots, width, height)
        t= 0
        while(not(size < room.getNumCleanedTiles())):
            for i in bots:
                anim.update(room, bots)
                i.updatePositionAndClean()
                if size == room.getNumCleanedTiles():
                    t+=1
                    break
            t+=1
        tr.append(t)
        room.cleanedTiles = []
        anim.done()
    sum = 0.0
    anim.done()
    anim.close()
    for i in tr:
        sum = sum + i
    return sum/num_trials
# === Problem 4

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newp = self.pos.getNewPosition(self.direction,self.speed)
        while(True):
            dec = self.room.isPositionInRoom(newp)
            if dec==True:
                x2 = int(newp.getX());
                y2 = int(newp.getY());
                x1 = int(self.pos.getX());
                y1 = int(self.pos.getY());
                for i in range(min(x1,x2),max(x1,x2)+1):
                    for j in range(min(y1,y2),max(y1,y2)+1):
                        p = (j*x2)-(j*x1)-(x2*y1)+(x1*y1)-(i*y2)+(x1*y2)+(i*y1)-(x1*y1)
                        if p==0:
                            if not(self.room.isTileCleaned(i,j)):
                                p = Position(i,j)
                                self.room.cleanTileAtPosition(p)
                self.setRobotPosition(self.room.getRandomPosition())
                self.setRobotDirection(int(random.random()*360))
                return
            else:
                self.setRobotDirection(int(random.random()*360))
                newp = self.room.getRandomPosition()
testRobotMovement(StandardRobot, RectangularRoom)

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        aa = runSimulation(num_robots, 1.0, 20, 20, 0.1, 20, StandardRobot)
        print "hgjg"
        times1.append(aa)
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.1, 20, RandomWalkRobot))
        print "over"
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
#showPlot1("Robot","Movements","Y axis")
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
showPlot2("plot2","x","y")
