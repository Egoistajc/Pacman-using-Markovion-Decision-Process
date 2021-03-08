# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with 
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util


"""
The class Grid is used as courtesy of the solution of week 5 mapAgent, which is basically written
by Simon Parsons. Some of the functions are being modified to better help the MDP process works
modified
"""
class Grid:
         
    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    def __init__(self, width, height, initial_grid = None):
        self.height = height
        self.width = width
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        
        # initial_grid is used to make a copy of the map
        if initial_grid != None:
            for i in range(self.height):
                for j in range(self.width):
                    self.grid[i][j] = initial_grid[i][j]

    # Print the grid out.
    def display(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
    
        
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices. Set value to the coordinate(x, y)
    def setValue(self, x, y, value):
        
        self.grid[y][x] = value

    # get the value of coordinate (x, y)
    def getValue(self, x, y):
        
        return self.grid[y][x]
    
    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def transferMap(self):
        newmap = Grid(self.width, self.height, self.grid)
        return newmap

    

# A Markovian Decision Process is a sequential decision problem for a 
# fully observable, stochastic environment with the transition model
# and additive rewards. The designing MDP agent runs in a non-deterministic
# environment and perform value iteration to achieve maximum expected utility
class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    # initialize the discount factor, initial utility, food value,
    # ghost value, reward and threshold between the changes of two
    # value iteration process
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"
        # initialize the dictionaries to store the variables of value iteration
        self.discountFactor = 0.92
        self.utility_init = 0
        self.foodVal = 1
        self.ghostVal = -1
        self.reward = -0.04
        self.epsilon = 0.001

        

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        print "I'm at:"
        print api.whereAmI(state)

        # Make a map of the right size
        self.mapSize(state)
        self.makeMap()
        # add wall, reward, food and ghosts in map
        self.addWallsToMap(state)
        self.rewardUpdate(state)
        self.updateFoodInMap(state)
        self.updateGhostToMap(state)
    
    # when rounds of game ended, clear the parameter and reset the internal state
    def final(self, state):
        print "This round of game is ended"
        self.mapSize(state)
        self.makeMap()
        # add wall, food, space and ghosts
        self.addWallsToMap(state)
        self.rewardUpdate(state)
        self.updateFoodInMap(state)
        self.updateGhostToMap(state)

    """
    combine the getLayoutHeight() and getLayoutWidth() method from the mapagent written
    by simon parson
    """  
    def mapSize(self, state):
            
            # use corner function from the api version 6 to calculate the size of the map
            corners = api.corners(state) 
            axis_X = []
            axis_y = []
            for corner in corners:
                axis_X.append(corner[0])
                axis_y.append(corner[1])
            self.width = max(axis_X) + 1
            self.height = max(axis_y) + 1

    """
    courtesy of makeMap function in mapagent written by simon parson
    """
    # Make a map by creating a grid of the right size
    def makeMap(self):
        self.map = Grid(self.width, self.height)

    # Functions to manipulate the map.
    "courtesy of the addWallsToMap function in mapAgent wriiten by simon parson in the AIN material"
    # Put every element in the list of wall elements into the map
    def addWallsToMap(self, state):
        wallList = api.walls(state)
        for wall in wallList:
            self.map.setValue(wall[0], wall[1], '%')
            
            

    # add a list of current food exist in the map
    def updateFoodInMap(self, state):
        foodList = api.food(state)
        for food in foodList:
            self.map.setValue(food[0], food[1], self.foodVal)
    
    # find the empty grid in the map
    def rewardUpdate(self, state):       
        for i in range(self.map.width):
            for j in range(self.map.height):
                if self.map.getValue(i, j) != '%':
                    self.map.setValue(i, j, self.utility_init)
                    
    

    def manhattanDistance(self, x1, y1, x2, y2):
            return int(abs(x1 - x2) + abs(y1 - y2))
            

    " Modified from api version 6 from AIN lab material: def ghostStates(state) "  
    def updateGhostToMap(self, state):

        ghosts = api.ghostStates(state)
        for ghost in ghosts:
            # if the state of ghost is scared
            if ghost[1] == 1 :
                continue
            else:
                # if the ghost is not scared
                self.map.setValue(int(ghost[0][0]), int(ghost[0][1]), self.ghostVal)
                

    """
    Ideas come from the def selectNewMove() in api version 6, and basically the process
    of calculating the expected utility from four directions is based on the AIN lecture
    
    """
    # calculate the expected utility heading north
    def northExpectedUtility(self, x, y):
        
        n = self.map.getValue(x, y + 1)
        e = self.map.getValue(x + 1, y)
        w = self.map.getValue(x - 1, y)
        s = self.map.getValue(x, y - 1)
        stay = self.map.getValue(x, y)
        # if the directions not in walls, calculate the utility of heading north
        if n != '%':
            true_north = 0.8 * n
        else:
            true_north = 0.8 * stay
        
        if e != '%':
            false_north_east = 0.1 * e
        else:
            false_north_east = 0.1 * stay

        if w != '%':
            false_north_west = 0.1 * w
        else:
            false_north_west = 0.1 * stay

        north_prime = true_north + false_north_east + false_north_west

        return north_prime

    ## calculate the expected utility heading east
    def eastExpectedUtility(self, x, y):    
        
        n = self.map.getValue(x, y + 1)
        e = self.map.getValue(x + 1, y)
        w = self.map.getValue(x - 1, y)
        s = self.map.getValue(x, y - 1)
        stay = self.map.getValue(x, y)

        # if the directions not in walls, calculate the utility of heading east
        if e != '%':
            true_east = 0.8 * e
        else:
            true_east = 0.8 * stay
            
        if n != '%':
            false_east_north = 0.1 * n
        else:
            false_east_north = 0.1 * stay 

        if s != '%':
            false_east_south = 0.1 * s
        else:
            false_east_south = 0.1 * stay
            
        east_prime = true_east + false_east_north + false_east_south 

        return east_prime

    # calculate the expected utility heading west
    def westExpectedUtility(self, x, y):   
        
        n = self.map.getValue(x, y + 1)
        e = self.map.getValue(x + 1, y)
        w = self.map.getValue(x - 1, y)
        s = self.map.getValue(x, y - 1)
        stay = self.map.getValue(x, y)

        # if the directions not in walls, calculate the utility of heading west
        if w != '%':
            true_west = 0.8 * w
        else:
            true_west = 0.8 * stay

        if s != '%':
            false_west_south = 0.1 * s
        else:
            false_west_south = 0.1 * stay  

        if n != '%':
            false_west_north = 0.1 * n
        else:
            false_west_north = 0.1 * stay
            
        west_prime = true_west + false_west_south + false_west_north 

        return west_prime

    # calculate the expected utility heading south
    def southExpectedUtility(self, x, y):    
        
        n = self.map.getValue(x, y + 1)
        e = self.map.getValue(x + 1, y)
        w = self.map.getValue(x - 1, y)
        s = self.map.getValue(x, y - 1)
        stay = self.map.getValue(x, y)

        # if the directions not in walls, calculate the utility of heading south
        if s != '%':
            true_south = 0.8 * s
        else:
            true_south = 0.8 * stay

        if e != '%':
            false_south_east = 0.1 * e
        else:
            false_south_east = 0.1 * stay  

        if w != '%':
            false_south_west = 0.1 * w
        else:
            false_south_west = 0.1 * stay
            
        south_prime = true_south + false_south_east + false_south_west 

        return south_prime
    
    # calculate the maximun expected utility based on the four expected utility 
    # on each direction. return the direction to make next move
    """ The idea on how to process the dictionary is modified from leyankoh on Github:
    https://github.com/leyankoh/pacman-mdp-solver/blob/master/mdpAgents.py. line 545-548
    """
    def MaximumExpectedUtility(self, x, y, IteratedDirection = False):
        north = self.northExpectedUtility(x, y)
        east = self.eastExpectedUtility(x, y)
        west = self.westExpectedUtility(x, y)
        south = self.southExpectedUtility(x, y)

        Dictation_Directions = {Directions.NORTH : north,Directions.WEST : west,Directions.SOUTH : south,Directions.EAST : east}

        MaximumVal = max(Dictation_Directions.values())

        if IteratedDirection == True:
            direction = max(Dictation_Directions, key = Dictation_Directions.get)
            return direction
        else:
            return MaximumVal

    # define the bellman equation and calcute the U(s) 
    def bellmanEquation(self, x, y):

        utility_state = self.discountFactor * self.MaximumExpectedUtility(x, y) + self.reward

        return utility_state


    # proceed the value interation of MDP
    def valueIteration(self):
        k = 1
        while k:
            # initialize a delta
            delta = 0
            # generate a blank map to store the current information
            self.newmap = self.map.transferMap() 
            # calculate the U(s) in black square          
            for i in range(self.width):
                for j in range(self.height):
                    if (self.map.getValue(i, j) != '%' and self.map.getValue(i, j) != self.ghostVal and self.map.getValue(i ,j) != self.foodVal):
                        # calcuter the U(s)
                        utility_state = self.bellmanEquation(i, j)
                        self.newmap.setValue(i, j, utility_state)
                        # if the difference between the iterated map and original map equals 
                        # to 0, then the MDP process should be stopped
                        if abs(self.newmap.getValue(i, j) - self.map.getValue(i, j)) > self.epsilon:
                            delta = abs(self.newmap.getValue(i, j) - self.map.getValue(i, j))
            # update the information of the current map            
            self.map = self.newmap.transferMap()

            if delta == 0:
                k = 0
    
    # move the pacman
    def getAction(self, state):
        
        self.rewardUpdate(state)
        self.updateFoodInMap(state)
        self.updateGhostToMap(state)
        self.valueIteration()
        # acquire the current coordinate of the pacman 
        pacman = api.whereAmI(state)
        axis_x = pacman[0]
        axis_y = pacman[1]

        #self.map.prettyDisplay()
        #show the iterated process

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # determine the next move
        return api.makeMove(self.MaximumExpectedUtility(axis_x, axis_y, True), legal)