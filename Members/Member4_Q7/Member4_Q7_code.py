# Q7 foodHeuristic  (goes into searchAgents.py)
# Excerpt of the final integrated code in Group_Project/search/. Not runnable on its own.

def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    # Q7 (Member 4): the true maze distance from Pacman to the farthest
    # remaining dot. Pacman must at least walk that far to eat that dot, so it
    # never overestimates (admissible). Maze distance obeys the triangle
    # inequality, so h(n) <= 1 + h(n') for any step (consistent). Distances
    # are memoised in problem.heuristicInfo so each BFS is run only once.
    food = foodGrid.asList()
    if not food:
        return 0
    cache = problem.heuristicInfo.setdefault('distCache', {})

    def dist(a, b):
        key = (a, b)
        if key not in cache:
            cache[key] = mazeDistance(a, b, problem.startingGameState)
        return cache[key]

    return max(dist(position, f) for f in food)
