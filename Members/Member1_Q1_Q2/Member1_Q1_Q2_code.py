# Q1 DFS + Q2 BFS  (goes into search.py)
# Excerpt of the final integrated code in Group_Project/search/. Not runnable on its own.

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
