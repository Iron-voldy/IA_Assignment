# Q3 UCS + Q4 A*  (goes into search.py)
# Excerpt of the final integrated code in Group_Project/search/. Not runnable on its own.

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
