# Member 1 - Q1 Depth First Search & Q2 Breadth First Search

**Name:** Member1  |  **Student ID:** IT23516101  |  **Group:** Group_XX

## What I was responsible for
Implemented the two uninformed graph-search algorithms that all later algorithms build on.

## Files / functions I edited
- `search.py` -> `depthFirstSearch(problem)` (Q1)
- `search.py` -> `breadthFirstSearch(problem)` (Q2)
- Full code: `Member1_Q1_Q2_code.py`
 
## How it works 
Both use the same graph-search skeleton: push `(state, path)` on the fringe, pop, return `path` if it is a goal, otherwise mark the state expanded and push unexpanded successors with `path + [action]`.
- **DFS** uses `util.Stack` (LIFO) -> goes deep first; finds *a* path, not necessarily the shortest.
- **BFS** uses `util.Queue` (FIFO) -> expands level by level; optimal when every step costs 1.
- The `expanded` set is what makes it *graph* search (no state expanded twice, so no infinite loops).

## Results (autograder, local run)
- Q1: PASS (146 nodes expanded on mediumMaze, path length 130) -> 4/4 marks
- Q2: PASS (269 nodes expanded on mediumMaze, path length 68) -> 4/4 marks

## How to run / verify
```
cd Group_Project/search
python autograder.py -q q1
python autograder.py -q q2
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
```

## Viva cheat-sheet (be ready to answer these)
- Why Stack vs Queue? What does each guarantee?
- Why do we need the expanded set? What happens without it?
- Is DFS optimal / complete? Is BFS? Time and space complexity (b, d, m)?
- Why check the goal when *popping* rather than when pushing?

## Team workflow
- Branch: work on your own feature branch, open a pull request into `main`.
- You review the pull request of **Member 2 (Q3-Q4)** and run their autograder question yourself.
- Before the viva, read ALL four code files and be able to explain every question.

## My Git work (commit each step separately, with your own account)
Suggested commits: "Add DFS with expanded set (Q1)", "Add BFS (Q2)", "Fix: return [] when fringe empty", "Add comments to DFS/BFS".

## AI usage
Claude Code (Sonnet 5) generated the first version of the whole project; I read, ran and reviewed the code. Exact prompts are listed in Section 8 of the report.
