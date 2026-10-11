# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py). 
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # Q1 (Member 1): graph-search DFS. The fringe is a LIFO Stack, so the most
    # recently discovered node is expanded first (deepest-first).
    fringe = util.Stack()
    fringe.push((problem.getStartState(), []))
    expanded = set()
    while not fringe.isEmpty():
        state, path = fringe.pop()
        if problem.isGoalState(state):
            return path
        if state not in expanded:
            expanded.add(state)
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in expanded:
                    fringe.push((successor, path + [action]))
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Q2 (Member 1): identical skeleton to DFS, but the fringe is a FIFO Queue,
    # so the shallowest node is expanded first (optimal for unit step costs).
    fringe = util.Queue()
    fringe.push((problem.getStartState(), []))
    expanded = set()
    while not fringe.isEmpty():
        state, path = fringe.pop()
        if problem.isGoalState(state):
            return path
        if state not in expanded:
            expanded.add(state)
            for successor, action, _ in problem.getSuccessors(state):
                if successor not in expanded:
                    fringe.push((successor, path + [action]))
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Q3 (Member 2): fringe is a PriorityQueue ordered by the accumulated path
    # cost g(n). A state is only finalised when it is popped (not when pushed),
    # which is what guarantees optimality with non-uniform step costs.
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)
    expanded = set()
    while not fringe.isEmpty():
        state, path, cost = fringe.pop()
        if problem.isGoalState(state):
            return path
        if state not in expanded:
            expanded.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in expanded:
                    newCost = cost + stepCost
                    fringe.push((successor, path + [action], newCost), newCost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Q4 (Member 2): same as UCS but the priority is f(n) = g(n) + h(n). With
    # nullHeuristic (h = 0) this degenerates to UCS; with an admissible and
    # consistent h it stays optimal while expanding fewer nodes.
    start = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push((start, [], 0), heuristic(start, problem))
    expanded = set()
    while not fringe.isEmpty():
        state, path, cost = fringe.pop()
        if problem.isGoalState(state):
            return path
        if state not in expanded:
            expanded.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in expanded:
                    newCost = cost + stepCost
                    fringe.push((successor, path + [action], newCost),
                                newCost + heuristic(successor, problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
