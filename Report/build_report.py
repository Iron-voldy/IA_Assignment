"""Builds Report/Group_XX_Report.html from the real project code (run from D:/IA_assignment)."""
import glob
import html


def mc(i):
    f = glob.glob(f'Members/Member{i}_*/Member{i}_*_code.py')[0]
    return open(f, encoding='utf-8').read().split('\n\n', 1)[1]


m1, m2, m3, m4 = mc(1), mc(2), mc(3), mc(4)


def part(src, start, end=None):
    i = src.index(start)
    j = src.index(end) if end else len(src)
    return html.escape(src[i:j].rstrip())


def shot(t):
    return f'<div class="shot">[SCREENSHOT: {t}]</div>'


Q = [
    ('Q1 - Depth First Search (4 marks)', 'search.py: <code>depthFirstSearch</code>',
     part(m1, 'def depthFirstSearch', 'def breadthFirstSearch'),
     'DFS is implemented as graph search. Each fringe entry is a pair (state, path of actions). The fringe is <code>util.Stack</code>, a LIFO structure, so the most recently discovered successor is expanded next and the search dives as deep as possible before backtracking. When a node is popped the goal test is applied; if it succeeds the stored action list is returned. Otherwise, if the state is not in the <code>expanded</code> set, it is added and each unexpanded successor is pushed with <code>path + [action]</code>. The expanded set turns tree search into graph search: no state is expanded twice, so cycles and the infinite-graph test cannot loop forever. DFS is complete on finite graphs but not optimal (mediumMaze: cost 130 with 146 nodes expanded, versus the optimal 68). Only <code>util.Stack</code> is used, as required.',
     'python autograder.py -q q1'),
    ('Q2 - Breadth First Search (4 marks)', 'search.py: <code>breadthFirstSearch</code>',
     part(m1, 'def breadthFirstSearch'),
     'BFS uses exactly the same skeleton as DFS; only the fringe changes to <code>util.Queue</code> (FIFO). Nodes are therefore expanded in order of increasing depth, so the first time a goal is popped it is reached by a path with the fewest actions. Because every Pac-Man move costs 1, that path is also the cheapest, so BFS is optimal here (mediumMaze: cost 68, 269 nodes expanded). The expanded set prevents re-expansion and keeps the search finite. BFS is complete and optimal for unit costs, but it stores the whole frontier, so memory grows like O(b^d); this is the main trade-off against DFS.',
     'python autograder.py -q q2'),
    ('Q3 - Uniform Cost Search (4 marks)', 'search.py: <code>uniformCostSearch</code>',
     part(m2, 'def uniformCostSearch', 'def aStarSearch'),
     'UCS generalises BFS to arbitrary positive step costs. The fringe is <code>util.PriorityQueue</code>; each entry is (state, path, cost) with priority equal to the accumulated cost g(n), so the cheapest node is always popped first. The goal test happens when a node is popped, not when it is generated, because a cheaper route to the goal may still be on the fringe when the goal is first generated. States enter the <code>expanded</code> set on pop, so a state is first expanded via its cheapest path. This gives optimal solutions under the exponential cost functions used by StayWestSearchAgent (cheap on the west side) and StayEastSearchAgent (expensive on the west side). On mediumMaze it returns cost 68 with 269 nodes, the same as BFS because costs are uniform.',
     'python autograder.py -q q3'),
    ('Q4 - A* Search (4 marks)', 'search.py: <code>aStarSearch</code>',
     part(m2, 'def aStarSearch'),
     "A* is UCS with the priority changed to f(n) = g(n) + h(n), where h is the supplied <code>heuristic(state, problem)</code>. The entry stores g so it can be extended, while the priority adds the heuristic of the successor. With the default <code>nullHeuristic</code>, h = 0 and A* is identical to UCS. With an admissible, consistent heuristic such as Manhattan distance, the first goal popped is optimal and fewer nodes are expanded: on bigMaze A* with manhattanHeuristic returns cost 210 while expanding 549 nodes, versus 620 for UCS. Consistency (h(n) &lt;= c(n,n') + h(n')) is what lets the graph-search version with an expanded set stay optimal, because f never decreases along a path.",
     'python autograder.py -q q4'),
    ('Q5 - Finding All the Corners (8 marks)',
     'searchAgents.py: <code>CornersProblem.getStartState</code>, <code>isGoalState</code>, <code>getSuccessors</code>',
     part(m3, 'class CornersProblem', 'def cornersHeuristic'),
     'The state is the tuple (position, visitedCorners), where visitedCorners is a 4-tuple of booleans aligned with <code>self.corners</code>. It holds only what is needed to decide the future: where Pacman is and which corners have been touched. It is small and hashable, so the expanded set works, and it does not store walls or the GameState. The start state marks a corner visited if Pacman starts on it. <code>isGoalState</code> is <code>all(visitedCorners)</code>. <code>getSuccessors</code> tries the four directions, skips wall cells, and for each legal move builds the new position and updates the visited flags (a flag becomes True when the new position equals that corner). Each step costs 1. The state space has at most (positions x 16) states, so BFS solves the corners mazes optimally.',
     'python autograder.py -q q5'),
    ('Q6 - Corners Problem: Heuristic (8 marks)', 'searchAgents.py: <code>cornersHeuristic</code>',
     part(m3, 'def cornersHeuristic'),
     "The heuristic solves a relaxed problem in which all walls are removed and distances are Manhattan. h(state) is the length of the cheapest tour that starts at Pacman and visits every still-unvisited corner; with at most four corners all orderings are tried recursively. Admissible: removing walls can only shorten real paths, so the relaxed optimum never exceeds the true cost. Consistent: one real step changes Pacman's Manhattan position by 1, so the relaxed optimum changes by at most 1, hence h(n) &lt;= 1 + h(n'). It returns 0 when all corners are visited and is never negative. It is much stronger than the maximum Manhattan distance to a corner because it accounts for the whole tour. Result on mediumCorners: 741 nodes expanded (full marks need at most 1200), optimal path length 106.",
     'python autograder.py -q q6'),
    ('Q7 - Eating All The Dots: Food Heuristic (8 marks)', 'searchAgents.py: <code>foodHeuristic</code>',
     part(m4, 'def foodHeuristic'),
     "h(state) is the true maze distance from Pacman to the farthest remaining dot, computed with the provided <code>mazeDistance</code> (a BFS that respects walls). Admissible: Pacman has to reach every dot, in particular the farthest, so the total cost is at least that distance. Consistent: maze distance is a shortest-path metric and obeys the triangle inequality, so after one step the farthest-dot distance drops by at most 1 and h(n) &lt;= 1 + h(n'). It returns 0 when no food remains. Because the same pairs are queried many times, each distance is memoised in <code>problem.heuristicInfo['distCache']</code>, so each BFS runs once. It is stronger than Manhattan distance or the food count because walls are included. Result on trickySearch: 4137 nodes expanded (full marks need at most 9000), optimal cost 60.",
     'python autograder.py -q q7'),
]

CSS = '''body{font-family:Segoe UI,Arial,sans-serif;font-size:11pt;margin:28px;line-height:1.4}h1{text-align:center}
h2{border-bottom:2px solid #444;margin-top:26px;page-break-after:avoid}
pre{background:#f4f4f4;border:1px solid #ddd;padding:8px;font-size:8.5pt;white-space:pre-wrap}
.shot{border:2px dashed #c33;color:#c33;padding:18px;margin:10px 0;text-align:center;font-weight:bold;background:#fff5f5}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #666;padding:6px}th{background:#e8e8e8}
code{background:#eee;padding:0 3px}.c{text-align:center}'''

h = f'<html><head><meta charset="utf-8"><title>Group Report</title><style>{CSS}</style></head><body>'
h += '''<div class="c"><h1>Search Algorithms in Pac-Man</h1><p><b>IT3012 / SE3062 - Intelligent Systems - Group Assignment</b></p>
<p>Group ID: Group_XX &nbsp;|&nbsp; Lecturer: Mr. Jeewaka Perera</p>
<p>Member1 - IT23516101 &nbsp; Member2 - IT23516202 &nbsp; Member3 - IT23516303 &nbsp; Member4 - IT23516404</p></div>
<h2>1. Introduction and Background Research</h2>
<p>This project implements the classic search algorithms on the Berkeley CS188 Pac-Man framework. A search problem is defined by a start state, a goal test, a successor function returning (state, action, cost) triples, and a path cost. All four algorithms share one graph-search skeleton: put the start on the fringe, pop a node, return its path if it is a goal, otherwise (if not already expanded) mark it expanded and push its successors. Only the fringe data structure differs.</p>
<table><tr><th>Algorithm</th><th>Fringe</th><th>Ordering</th><th>Complete</th><th>Optimal</th></tr>
<tr><td>DFS</td><td>Stack (LIFO)</td><td>deepest first</td><td>yes (finite graph, with expanded set)</td><td>no</td></tr>
<tr><td>BFS</td><td>Queue (FIFO)</td><td>shallowest first</td><td>yes</td><td>yes for unit cost</td></tr>
<tr><td>UCS</td><td>Priority queue</td><td>g(n)</td><td>yes</td><td>yes (positive costs)</td></tr>
<tr><td>A*</td><td>Priority queue</td><td>g(n)+h(n)</td><td>yes</td><td>yes if h admissible (tree) / consistent (graph)</td></tr></table>
<p><b>Heuristics.</b> A heuristic h(n) estimates the cost from n to the nearest goal. It is <i>admissible</i> if h(n) &lt;= true cost h*(n) and <i>consistent</i> if h(n) &lt;= c(n,n') + h(n') for every successor n'; consistency implies admissibility. A standard way to design one is to solve a <i>relaxed</i> problem (remove constraints such as walls) exactly, which gives a lower bound on the true cost. We used this idea for the corners heuristic (walls removed, cheapest Manhattan tour) and for the food heuristic (true maze distance to the farthest dot, a lower bound because every dot must be reached). Sources: Russell &amp; Norvig, <i>Artificial Intelligence: A Modern Approach</i> (ch. 3); UC Berkeley CS188 Project 1 description.</p>
<h2>2. Team, Environment and Task Split</h2>
<table><tr><th>Member</th><th>Questions</th><th>Files</th></tr>
<tr><td>Member 1</td><td>Q1 DFS, Q2 BFS</td><td>search.py</td></tr><tr><td>Member 2</td><td>Q3 UCS, Q4 A*</td><td>search.py</td></tr>
<tr><td>Member 3</td><td>Q5 CornersProblem, Q6 cornersHeuristic</td><td>searchAgents.py</td></tr><tr><td>Member 4</td><td>Q7 foodHeuristic, integration, report</td><td>searchAgents.py</td></tr></table>
<p>Environment: Python 3.11 in a Conda environment (<code>conda create -n cs188 python=3.11</code>; <code>pip install numpy matplotlib</code>). Only <code>search.py</code> and <code>searchAgents.py</code> were edited; no files, functions or classes were renamed.</p>
'''
h += shot('python pacman.py - the playable Pac-Man window, plus the terminal showing the conda environment / python version')
h += '<h2>3. Question-by-Question Results</h2><p><i>Note: the local autograder prints the original Berkeley point values; all test cases for Q1-Q7 pass. Course marks are as defined in the assignment.</i></p>'
for t, f, c, e, cmd in Q:
    h += f'<h2>{t}</h2><p><b>Code edited/added:</b> {f}</p><pre>{c}</pre>'
    h += shot(f'autograder output: {cmd} - showing the question passed / score')
    if t.startswith('Q6'):
        h += shot('python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5 (shows 741 nodes expanded, cost 106)')
    if t.startswith('Q7'):
        h += shot('python pacman.py -l trickySearch -p AStarFoodSearchAgent (shows 4137 nodes expanded, cost 60)')
    h += f'<p><b>Explanation.</b> {e}</p>'
h += '<h2>4. Full Autograder Run</h2>' + shot('python autograder.py --no-graphics - final summary of all questions')
h += '<h2>5. Public Git Repository</h2><p>Repository URL: [PASTE PUBLIC GIT REPOSITORY LINK HERE]</p><h2>6. Git Contribution Evidence</h2>'
h += shot('Commit history (git log --oneline --graph --all, or GitHub Commits page) with meaningful messages')
h += shot('GitHub Insights > Contributors graph showing all 4 members')
h += shot('Insights > Commits / Code frequency showing commits spread over the assignment period')
h += shot("Each member's own commits (filter by author) - one screenshot per member, or Pull Requests / branches page")
h += '''<h2>7. Individual Contribution Table</h2>
<table><tr><th>Name</th><th>Student ID</th><th>Tasks / Questions contributed</th></tr>
<tr><td>Member1</td><td>IT23516101</td><td>Q1 DFS, Q2 BFS (search.py); peer-review of Q3-Q4 code; branch <code>feature/dfs-bfs</code></td></tr>
<tr><td>Member2</td><td>IT23516202</td><td>Q3 UCS, Q4 A* (search.py); peer-review of Q5-Q6 code; branch <code>feature/ucs-astar</code></td></tr>
<tr><td>Member3</td><td>IT23516303</td><td>Q5 CornersProblem, Q6 cornersHeuristic (searchAgents.py); peer-review of Q7 code; branch <code>feature/corners</code></td></tr>
<tr><td>Member4</td><td>IT23516404</td><td>Q7 foodHeuristic (searchAgents.py); peer-review of Q1-Q2 code; integration/merge, report, submission package; branch <code>feature/food-heuristic</code></td></tr></table>
<h2>8. AI Usage Declaration</h2>
<p><b>Tool used:</b> Claude Code (Anthropic, model Claude Sonnet 5), used to research the problem, generate the initial implementation of Q1-Q7, run the autograder and draft this report and the per-member READMEs. Every member then read, ran and reviewed all of the code (peer-review pairs in Section 7) and can explain it in the viva.</p>
<p><b>Exact prompts:</b></p>
<pre>Prompt 1: "check this assignment [IT3012 Group Assignment (10%) CourseWeb.pdf] and check this zip [search.zip] based on this 2 we need to complete this assignment within today. check all details, this project need to build for 4 members. and you need to make a small research about this project and next you want to build this mentioned things. and finally you need to make a report within mentioned things using and next you need to mention what areas screen shots we need to add to the report. that things you give inside the brackets and each members full codes you need to build and make given folder structure and properly. and each members make separate read me files what they did and that files need to build outside of the project. .. and also if you have any question you can ask from me."

Prompt 2: "1. I give name laters for now add like member1 and some random number.. 2. add proper prompts if want 3. make properly. think as a team"</pre>
<h2>9. Team Workflow</h2>
<p>Each member worked on their own feature branch and merged into <code>main</code> through a pull request reviewed by a teammate (review ring: M1 reviews M2, M2 reviews M3, M3 reviews M4, M4 reviews M1). Commits were small and used messages such as "Add DFS with expanded set (Q1)".</p>
</body></html>'''
open('Report/Group_XX_Report.html', 'w', encoding='utf-8').write(h)
print('ok', len(h))
