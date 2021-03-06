# sampleAgents.py
# parsons/07-oct-2017
#
# Version 1.1
#
# Some simple agents to work with the PacMan AI projects from:
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

# The agents here are extensions written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

# RandomAgent
#
# A very simple agent. Just makes a random pick every time that it is
# asked for an action.
class RandomAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Random choice between the legal options.
        return api.makeMove(random.choice(legal), legal)

# RandomishAgent
#
# A tiny bit more sophisticated. Having picked a direction, keep going
# until that direction is no longer possible. Then make a random
# choice.
class RandomishAgent(Agent):

    # Constructor
    #
    # Create a variable to hold the last action
    def __init__(self):
         self.last = Directions.STOP
    
    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # If we can repeat the last action, do it. Otherwise make a
        # random choice.
        if self.last in legal:
            return api.makeMove(self.last, legal)
        else:
            pick = random.choice(legal)
            # Since we changed action, record what we did
            self.last = pick
            return api.makeMove(pick, legal)

# SensingAgent
#
# Doesn't move, but reports sensory data available to Pacman
class SensingAgent(Agent):

    def getAction(self, state):

        # Demonstrates the information that Pacman can access about the state
        # of the game.

        # What are the current moves available
        legal = api.legalActions(state)
        print "Legal moves: ", legal

        # Where is Pacman?
        pacman = api.whereAmI(state)
        print "Pacman position: ", pacman

        # Where are the ghosts?
        print "Ghost positions:"
        theGhosts = api.ghosts(state)
        for i in range(len(theGhosts)):
            print theGhosts[i]

        # How far away are the ghosts?
        print "Distance to ghosts:"
        for i in range(len(theGhosts)):
            print util.manhattanDistance(pacman,theGhosts[i])

        # Where are the capsules?
        print "Capsule locations:"
        print api.capsules(state)
        
        # Where is the food?
        print "Food locations: "
        print api.food(state)

        # Where are the walls?
        print "Wall locations: "
        print api.walls(state)
        
        # getAction has to return a move. Here we pass "STOP" to the
        # API to ask Pacman to stay where they are.
        return api.makeMove(Directions.STOP, legal)


class CornerSeekingAgent(Agent):


# Constructor
#
# Create variables to remember target positions
    def __init__(self):
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False


    def final(self, state):
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False


    def getAction(self, state):
        # Get extreme x and y values for the grid
        corners = api.corners(state)
        print
        corners
        # Setup variable to hold the values
        minX = 100
        minY = 100
        maxX = 0
        maxY = 0

        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]

            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY

        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        print
        legal
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Where is Pacman now?
        pacman = api.whereAmI(state)
        print
        pacman
        #
        # If we haven't got to the lower left corner, try to do that
        #

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                print
                "Got to BL!"
                self.BL = True

        # If not, move towards it, first to the West, then to the South.
        if self.BL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
        #
        # Now we've got the lower left corner
        #

        # Move towards the top left corner

        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == maxY - 1:
                print
                "Got to TL!"
                self.TL = True

        # If not, move West then North.
        if self.TL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Now, the top right corner

        # Check we aren't there:
        if pacman[0] == maxX - 1:
            if pacman[1] == maxY - 1:
                print
                "Got to TR!"
                self.TR = True

        # Move east where possible, then North
        if self.TR == False:
            if pacman[0] < maxX - 1:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Fromto right it is a straight shot South to get to the bottom right.

        if pacman[0] == maxX - 1:
            if pacman[1] == minY + 1:
                print
                "Got to BR!"
                self.BR = True
                return api.makeMove(Directions.STOP, legal)
            else:
                print
                "Nearly there"
                return api.makeMove(Directions.SOUTH, legal)

        print
        "Not doing anything!"
        return api.makeMove(Directions.STOP, legal)

class GoWestAgent(Agent):

    def getAction(self, state):
        # Get the actions we can try, and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        # Go west if possible
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        # Otherwise make a random choice
        else:
            pick = random.choice(legal)
            return api.makeMove(pick, legal)

class HungryAgent(Agent):
	#Pacman moves towards the closest food he senses
	#though he is unable to get himself past walls...
	#if he doesn't smell any food close to him that he can legally access, he moves in a random direction then
	#continues from there

	def getAction(self, state):

		legal = state.getLegalPacmanActions() #Again, get a list of pacman's legal actions
		if Directions.STOP in legal:
			legal.remove(Directions.STOP)
		pacman = api.whereAmI(state) #retrieve location of pacman
		food = api.food(state) #retrieve location of food

		#Distance of food
		dist = [] # initiate list of distances
		for i in range(len(food)):
			dist.append(util.manhattanDistance(pacman, food[i]))

		minIndex = dist.index(min(dist)) #get index of min dist value (assuming the array remains ordered)
		closestFood = food[minIndex]

		#current position coordinates
		x1, y1 = pacman[0], pacman[1]
		x2, y2 = closestFood

		print "closest food is: "
		print closestFood
		print "pacman's location is: "
		print pacman

		print "list of distances: "
		print dist

		#if pacman is to the West of closest food, then goEast = True and so on...
		goEast = x1 < x2 and y1 == y2
		goWest = x1 > x2 and y1 == y2
		goNorth = x1 == x2 and y1 < y2
		goSouth = x1 == x2 and y1 > y2

		last = state.getPacmanState().configuration.direction

		if x1 == 9 and y1 == 1:
			return api.makeMove(random.choice(legal), legal)
		else:
			pass

		if Directions.EAST in legal and (goEast):
			return api.makeMove('East', legal)

		elif Directions.WEST in legal and (goWest):
			return api.makeMove('West', legal)

		elif Directions.NORTH in legal and (goNorth):
			return api.makeMove('North', legal)

		elif Directions.SOUTH in legal and (goSouth):
			return api.makeMove('South', legal)

		elif last in legal:                   #if pacman doesnt find a move he can do, he just repeats the last move.
			return api.makeMove(last, legal)  #this makes it so that the closest food isn't across the wall from him next

		else:
			return api.makeMove(random.choice(legal), legal) #just return a random move when he's out of moves

class SurvivalAgent(Agent):

    def getAction(self, state):
        pass
    
class SurvivalAgent(Agent):
	#This agent runs away from ghosts
	#when he senses that ghosts are within range (distance <= 5)
	#Otherwise, like hungry agent, he forages for food

	def getAction(self, state):
		ghosts = api.ghosts(state) #get state of ghosts
		legal = state.getLegalPacmanActions() #Again, get a list of pacman's legal actions
		pacman = api.whereAmI(state) #retrieve location of pacman
		food = api.food(state) #retrieve location of food
		last = state.getPacmanState().configuration.direction #store last move

		#remove stop
		if Directions.STOP in legal:
			legal.remove(Directions.STOP)

		gDist = [] #get distance from ghosts
		for i in range(len(ghosts)):
			gDist.append(util.manhattanDistance(pacman, ghosts[i]))

		minIndex = gDist.index(min(gDist)) #get index of min dist to ghost value
		closestGhost = ghosts[minIndex] #returns x,y of closest ghost

		####Hungry agent####
		#Distance of food
		dist = [] # initiate list of distances
		for i in range(len(food)):
			dist.append(util.manhattanDistance(pacman, food[i]))

		minIndex = dist.index(min(dist)) #get index of min dist value (assuming the array remains ordered)
		closestFood = food[minIndex]

		#current position coordinates
		x1, y1 = pacman[0], pacman[1]
		x2, y2 = closestFood
		x3, y3 = closestGhost

		print "-" * 15
		print "closest food is: "
		print closestFood
		print "list of distances: "
		print dist
		print "Location of pacman: "
		print pacman
		print "Location of ghosts: "
		print ghosts
		print "Distance to ghosts: "
		print gDist
		print "Closest ghost: "
		print closestGhost
		print "Food Map: "
		print food

		if min(gDist) > 5:
		#if pacman is to the West of closest food, then goEast = True and so on...
			goEast = x1 < x2 and y1 == y2
			goWest = x1 > x2 and y1 == y2
			goNorth = x1 == x2 and y1 < y2
			goSouth = x1 == x2 and y1 > y2

			if x1 == 9 and y1 == 1:
				return api.makeMove(random.choice(legal), legal)
			else:
				pass

			if Directions.EAST in legal and (goEast):
				return api.makeMove('East', legal)

			elif Directions.WEST in legal and (goWest):
				return api.makeMove('West', legal)

			elif Directions.NORTH in legal and (goNorth):
				return api.makeMove('North', legal)

			elif Directions.SOUTH in legal and (goSouth):
				return api.makeMove('South', legal)

			elif last in legal:                   #if pacman doesnt find a move he can do, he just repeats the last move.
				return api.makeMove(last, legal)  #this makes it so that the closest food isn't across the wall from him next

			else:
				return api.makeMove(random.choice(legal), legal) #just return a random move when he's out of moves

		#these directions would be opposite of HungryAgent
		#mainly because you are trying to run away
		else:
			warnEast = x1 > x3 and y1 == y3
			warnWest = x1 < x3 and y1 == y3
			warnNorth = x1 == x3 and y1 > y3
			warnSouth = x1 == x3 and y1 < y3

			if Directions.EAST in legal and (warnEast):
				return api.makeMove('East', legal)

			elif Directions.WEST in legal and (warnWest):
				return api.makeMove('West', legal)

			elif Directions.NORTH in legal and (warnNorth):
				return api.makeMove('North', legal)

			elif Directions.SOUTH in legal and (warnSouth):
				return api.makeMove('South', legal)

			elif last in legal:                   #if pacman doesnt find a move he can do, he just repeats the last move.
				return api.makeMove(last, legal)  #this makes it so that the closest food isn't across the wall from him next

			else:
				return api.makeMove(random.choice(legal), legal) #just return a random move when he's out of moves
