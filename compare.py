from itertools import combinations
from pathlib import Path

from mmsim.mazes import load_maze


# Load mazes
data = {}
for maze in Path('classic').glob('*.txt'):
    data[maze.name] = load_maze(maze)

# Compare mazes
for (a_name, a_data), (b_name, b_data) in combinations(data.items(), 2):
    diff = abs(a_data - b_data).astype(bool).sum()
    if diff <= 2:
        print('%d:\n  %s\n  %s' % (diff, a_name, b_name))
