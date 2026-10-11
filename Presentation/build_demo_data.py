"""
Runs our real search code (search.py / searchAgents.py) on the same layouts the
assignment uses and records, for each question, the order in which Pac-Man
positions were expanded and the final path. The output, demo_data.js, drives
the animated maze replays in index.html.

Run from the repo root:   python Presentation/build_demo_data.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIR = os.path.join(HERE, '..', 'Group_Project', 'search')
sys.path.insert(0, SEARCH_DIR)
os.chdir(SEARCH_DIR)  # layout.getLayout looks in ./layouts

import layout
import pacman
import search
import searchAgents
from game import Actions


def make_state(name):
    lay = layout.getLayout(name)
    state = pacman.GameState()
    state.initialize(lay, 0)
    return lay, state


def position_of(s):
    # PositionSearchProblem states are (x, y); the other problems are (pos, extra).
    return s if isinstance(s[0], int) else s[0]


def record(problem, search_fn):
    """Wrap getSuccessors so every expansion is logged in order."""
    order = []
    original = problem.getSuccessors

    def logged(s):
        order.append(list(position_of(s)))
        return original(s)

    problem.getSuccessors = logged
    actions = search_fn(problem)
    x, y = position_of(problem.getStartState())
    path = [[x, y]]
    for a in actions:
        dx, dy = Actions.directionToVector(a)
        x, y = int(x + dx), int(y + dy)
        path.append([x, y])
    return order, path, actions


def demo(name, lay, problem, search_fn, cost=None):
    order, path, actions = record(problem, search_fn)
    w, h = lay.width, lay.height
    walls = [[x, y] for x in range(w) for y in range(h) if lay.walls[x][y]]
    food = [[x, y] for x in range(w) for y in range(h) if lay.food[x][y]]
    return {
        'layout': name, 'w': w, 'h': h, 'walls': walls, 'food': food,
        'expanded': order, 'path': path,
        'nodes': len(order),
        'cost': cost if cost is not None else problem.getCostOfActions(actions),
    }


def main():
    data = {}

    lay, st = make_state('mediumMaze')
    data['q1'] = demo('mediumMaze', lay, searchAgents.PositionSearchProblem(st, warn=False, visualize=False), search.dfs)
    lay, st = make_state('mediumMaze')
    data['q2'] = demo('mediumMaze', lay, searchAgents.PositionSearchProblem(st, warn=False, visualize=False), search.bfs)

    # Q3: StayEastSearchAgent's cost function, 0.5 ** x (cheap on the east side).
    lay, st = make_state('mediumDottedMaze')
    prob = searchAgents.PositionSearchProblem(st, costFn=lambda pos: .5 ** pos[0], warn=False, visualize=False)
    data['q3'] = demo('mediumDottedMaze', lay, prob, search.ucs)
    data['q3']['cost'] = round(data['q3']['cost'], 4)

    lay, st = make_state('bigMaze')
    data['q4'] = demo('bigMaze', lay, searchAgents.PositionSearchProblem(st, warn=False, visualize=False),
                      lambda p: search.astar(p, searchAgents.manhattanHeuristic))
    lay, st = make_state('bigMaze')
    data['q4']['ucsNodes'] = demo('bigMaze', lay, searchAgents.PositionSearchProblem(st, warn=False, visualize=False),
                                  search.ucs)['nodes']

    lay, st = make_state('mediumCorners')
    data['q5'] = demo('mediumCorners', lay, searchAgents.CornersProblem(st), search.bfs)
    lay, st = make_state('mediumCorners')
    data['q6'] = demo('mediumCorners', lay, searchAgents.CornersProblem(st),
                      lambda p: search.astar(p, searchAgents.cornersHeuristic))

    lay, st = make_state('trickySearch')
    data['q7'] = demo('trickySearch', lay, searchAgents.FoodSearchProblem(st),
                      lambda p: search.astar(p, searchAgents.foodHeuristic))

    out = os.path.join(HERE, 'demo_data.js')
    with open(out, 'w') as f:
        f.write('window.DEMO = ' + json.dumps(data, separators=(',', ':')) + ';\n')
    for q, d in data.items():
        print(q, d['layout'], 'nodes', d['nodes'], 'cost', d['cost'], 'path', len(d['path']) - 1)


if __name__ == '__main__':
    main()
