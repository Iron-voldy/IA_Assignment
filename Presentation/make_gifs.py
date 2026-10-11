"""
Turns demo_data.js (recorded by build_demo_data.py) into one animated GIF per
question, saved in Presentation/media/. Each GIF shows the cells our search
expanded, in the real order, then Pac-Man walking the path it returned.

Run from the repo root:   python Presentation/make_gifs.py
"""
import json
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'media')

BG = (7, 9, 20)
WALL = (27, 38, 120)
WALL_EDGE = (77, 104, 255)
FOOD = (255, 214, 170)
PATH = (255, 214, 0)
# Each member's questions use that member's ghost colour.
GHOST = {'q1': (255, 70, 70), 'q2': (255, 70, 70), 'q3': (255, 140, 210), 'q4': (255, 140, 210),
         'q5': (60, 220, 255), 'q6': (60, 220, 255), 'q7': (255, 170, 60)}


def load():
    with open(os.path.join(HERE, 'demo_data.js')) as f:
        text = f.read()
    return json.loads(text[text.index('{'):text.rstrip().rindex(';')])


def render(q, d, cell):
    w, h = d['w'], d['h']
    W, H = w * cell, h * cell
    walls = {tuple(p) for p in d['walls']}
    food = [tuple(p) for p in d['food']]
    expanded, path = d['expanded'], [tuple(p) for p in d['path']]
    tint = GHOST[q]

    def box(x, y):  # game y=0 is the bottom row
        top = (h - 1 - y) * cell
        return [x * cell, top, x * cell + cell - 1, top + cell - 1]

    base = Image.new('RGB', (W, H), BG)
    dr = ImageDraw.Draw(base)
    for (x, y) in walls:
        dr.rectangle(box(x, y), fill=WALL, outline=WALL_EDGE)

    def frame(n_expanded, n_path):
        im = base.copy()
        dr = ImageDraw.Draw(im)
        counts = {}
        for p in expanded[:n_expanded]:
            counts[tuple(p)] = counts.get(tuple(p), 0) + 1
        for (x, y), c in counts.items():
            a = min(1.0, 0.35 + 0.15 * c)
            col = tuple(int(BG[i] + (tint[i] - BG[i]) * a * 0.75) for i in range(3))
            b = box(x, y)
            dr.rectangle([b[0] + 1, b[1] + 1, b[2] - 1, b[3] - 1], fill=col)
        eaten = set(path[:n_path + 1]) if n_path else set()
        r = max(1, cell // 6)
        for (x, y) in food:
            if (x, y) in eaten:
                continue
            cx, cy = x * cell + cell / 2, (h - 1 - y) * cell + cell / 2
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=FOOD)
        if n_path:
            pts = [(x * cell + cell / 2, (h - 1 - y) * cell + cell / 2) for (x, y) in path[:n_path + 1]]
            if len(pts) > 1:
                dr.line(pts, fill=PATH, width=max(2, cell // 5))
            px, py = pts[-1]
            pr = cell * 0.42
            dr.pieslice([px - pr, py - pr, px + pr, py + pr], 30, 330, fill=PATH)
        return im

    frames = []
    steps = 50
    for i in range(1, steps + 1):
        frames.append(frame(round(len(expanded) * i / steps), 0))
    psteps = min(60, len(path) - 1)
    for i in range(1, psteps + 1):
        frames.append(frame(len(expanded), round((len(path) - 1) * i / psteps)))
    durations = [40] * steps + [45] * psteps
    durations[-1] = 1800
    frames[0].save(os.path.join(OUT, q + '.gif'), save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    data = load()
    for q, d in data.items():
        cell = 22 if d['w'] <= 20 else (10 if d['w'] > 36 else 14)
        render(q, d, cell)
        print('wrote', q + '.gif', os.path.getsize(os.path.join(OUT, q + '.gif')) // 1024, 'KB')


if __name__ == '__main__':
    main()
