"""
Q7 evidence (Member 4): runs our A* on trickySearch with five different food
heuristics and prints how many nodes each one expands. Also measures how much
the distance cache in foodHeuristic saves.

Run from the repo root:   python Presentation/compare_food_heuristics.py
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIR = os.path.join(HERE, '..', 'Group_Project', 'search')
sys.path.insert(0, SEARCH_DIR)
os.chdir(SEARCH_DIR)  # layout.getLayout looks in ./layouts

import layout
import pacman
import search
import searchAgents


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---- the heuristics we compare -------------------------------------------
def no_heuristic(state, problem):
    return 0


def dots_left(state, problem):
    return len(state[1].asList())


def farthest_manhattan(state, problem):
    position, foodGrid = state
    return max([manhattan(position, f) for f in foodGrid.asList()], default=0)


def sum_manhattan(state, problem):
    # NOT admissible: one walk eats many dots, so steps are counted many times.
    position, foodGrid = state
    return sum(manhattan(position, f) for f in foodGrid.asList())


HEURISTICS = [
    ('No guess (h = 0, same as UCS)', no_heuristic, 'yes'),
    ('Number of dots left', dots_left, 'yes'),
    ('Farthest dot, Manhattan', farthest_manhattan, 'yes'),
    ('Farthest dot, maze distance (OURS)', searchAgents.foodHeuristic, 'yes'),
    ('Sum of Manhattan distances', sum_manhattan, 'NO - can guess too high'),
]


def new_problem(gameState):
    return searchAgents.FoodSearchProblem(gameState)


def main(layout_name='trickySearch'):
    lay = layout.getLayout(layout_name)
    gameState = pacman.GameState()
    gameState.initialize(lay, 0)

    print(f'A* on {layout_name}  ({len(gameState.getFood().asList())} dots)\n')
    print(f'{"Heuristic":38s} {"Nodes":>8s} {"Path":>6s} {"Time":>7s}  Admissible?')
    print('-' * 78)
    for name, h, admissible in HEURISTICS:
        problem = new_problem(gameState)
        start = time.time()
        actions = search.aStarSearch(problem, h)
        took = time.time() - start
        print(f'{name:38s} {problem._expanded:8d} {len(actions):6d} {took:6.2f}s  {admissible}')

    # ---- cache on vs off -------------------------------------------------
    calls = [0]
    real_maze_distance = searchAgents.mazeDistance

    def counted_maze_distance(a, b, gs):
        calls[0] += 1
        return real_maze_distance(a, b, gs)

    def farthest_maze_no_cache(state, problem):
        position, foodGrid = state
        return max([counted_maze_distance(position, f, problem.startingGameState)
                    for f in foodGrid.asList()], default=0)

    problem = new_problem(gameState)
    start = time.time()
    search.aStarSearch(problem, farthest_maze_no_cache)
    no_cache_time, no_cache_calls = time.time() - start, calls[0]

    problem = new_problem(gameState)
    start = time.time()
    search.aStarSearch(problem, searchAgents.foodHeuristic)
    cache_time = time.time() - start
    cache_calls = len(problem.heuristicInfo['distCache'])

    print('\nDistance cache (problem.heuristicInfo):')
    print(f'  without cache: {no_cache_calls:6d} BFS runs  {no_cache_time:5.2f}s')
    print(f'  with cache:    {cache_calls:6d} BFS runs  {cache_time:5.2f}s')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'trickySearch')
