"""
Opens the real Pac-Man game window for each member's part, one after another,
so every member can show their own question running.

Run from the repo root:
    python Presentation/run_member_demos.py          # menu
    python Presentation/run_member_demos.py 4        # all of Member 4's demos
    python Presentation/run_member_demos.py q7       # just one question
    python Presentation/run_member_demos.py all      # every demo, Q1 -> Q7

Close the game window (or let it finish) to move on to the next demo.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH_DIR = os.path.join(HERE, '..', 'Group_Project', 'search')

# question -> (member, what it shows, pacman.py arguments)
DEMOS = {
    'q1': (1, 'DFS on mediumMaze (dives deep, 130 steps)',
           ['-l', 'mediumMaze', '-p', 'SearchAgent', '-a', 'fn=dfs']),
    'q2': (1, 'BFS on mediumMaze (shortest path, 68 steps)',
           ['-l', 'mediumMaze', '-p', 'SearchAgent', '-a', 'fn=bfs']),
    'q3': (2, 'UCS on mediumDottedMaze (east side is cheap)',
           ['-l', 'mediumDottedMaze', '-p', 'StayEastSearchAgent']),
    'q4': (2, 'A* + Manhattan on bigMaze (549 nodes vs 620 for UCS)',
           ['-l', 'bigMaze', '-z', '.5', '-p', 'SearchAgent',
            '-a', 'fn=astar,heuristic=manhattanHeuristic']),
    'q5': (3, 'Corners problem with BFS on mediumCorners',
           ['-l', 'mediumCorners', '-p', 'SearchAgent',
            '-a', 'fn=bfs,prob=CornersProblem']),
    'q6': (3, 'Corners heuristic with A* (741 nodes)',
           ['-l', 'mediumCorners', '-p', 'AStarCornersAgent', '-z', '0.5']),
    'q7': (4, 'Food heuristic with A* on trickySearch (4137 nodes)',
           ['-l', 'trickySearch', '-p', 'AStarFoodSearchAgent']),
}


def run(q):
    member, what, args = DEMOS[q]
    print(f'\n=== Member {member} - {q.upper()}: {what}')
    print('    python pacman.py ' + ' '.join(args))
    # pacman.py prints "Path found with total cost ... Search nodes expanded ..."
    subprocess.run([sys.executable, 'pacman.py', *args, '--frameTime', '0.05'],
                   cwd=SEARCH_DIR)


def pick(choice):
    choice = choice.lower().strip()
    if choice == 'all':
        return list(DEMOS)
    if choice in DEMOS:
        return [choice]
    if choice.isdigit():
        return [q for q, (m, _, _) in DEMOS.items() if m == int(choice)]
    return []


def main():
    choice = sys.argv[1] if len(sys.argv) > 1 else None
    if choice is None:
        for q, (m, what, _) in DEMOS.items():
            print(f'  {q}  Member {m}  {what}')
        choice = input('\nType a question (q1-q7), a member number (1-4) or "all": ')
    todo = pick(choice)
    if not todo:
        print('Nothing matched. Use q1-q7, 1-4 or all.')
        return
    for q in todo:
        run(q)


if __name__ == '__main__':
    main()
