# Q5 CornersProblem + Q6 cornersHeuristic  (goes into searchAgents.py)
# Excerpt of the final integrated code in Group_Project/search/. Not runnable on its own.

# Author: Member 3 (Q5 and Q6)
# Q5 defines the state space for the corners problem; Q6 adds its A* heuristic.

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState: pacman.GameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        # Q5 (Member 3): state = (position, visitedCorners). visitedCorners is a
        # tuple of 4 booleans aligned with self.corners, so the state is small
        # and hashable and contains no walls / GameState.
        # One boolean per corner, True if Pacman already starts on that corner.
        visited = tuple(self.startingPosition == c for c in self.corners)
        return (self.startingPosition, visited)

    def isGoalState(self, state: Any):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        return all(state[1])

    def getSuccessors(self, state: Any):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            "*** YOUR CODE HERE ***"
            # Unpack the current position and visited flags; every legal move costs 1.
            (x, y), visited = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextPos = (nextx, nexty)
                # Mark a corner as visited when Pacman steps onto it.
                newVisited = tuple(v or nextPos == c
                                   for v, c in zip(visited, self.corners))
                successors.append(((nextPos, newVisited), action, 1))

        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state: Any, problem: CornersProblem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    "*** YOUR CODE HERE ***"
    # Q6 (Member 3): relax the problem by deleting the walls. The heuristic is
    # the cost of the cheapest tour (Manhattan distances) that starts at
    # Pacman and visits every unvisited corner. That is the exact optimum of
    # the relaxed problem, hence admissible; and it is consistent because a
    # single real step changes the relaxed optimum by at most 1.
    position, visited = state
    remaining = [c for c, v in zip(corners, visited) if not v]
    if not remaining:
        return 0

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Brute-force recursion over the order of the remaining corners (at most 4! orders),
    # so the cost is tiny. Walls are ignored, which keeps the value a lower bound.
    def cheapestTour(current, todo):
        if not todo:
            return 0
        return min(manhattan(current, c) + cheapestTour(c, [r for r in todo if r != c])
                   for c in todo)

    return cheapestTour(position, remaining)
