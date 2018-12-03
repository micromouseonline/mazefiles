"""
Basic tests to ensure maze files are properly formatted.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import re

import pytest


def parametrize_maze_files(maze_files):
    return pytest.mark.parametrize('maze_file', maze_files,
                                   ids=[str(x) for x in maze_files])


CLASSIC_SIZE = 16
HALFSIZE_SIZE = 32

classic_mazes = list(Path('classic').glob('*'))
halfsize_mazes = list(Path('halfsize').glob('*'))
training_mazes = list(Path('training').glob('*'))
competition_mazes = classic_mazes + halfsize_mazes
all_mazes = classic_mazes + halfsize_mazes + training_mazes

classic_mazes = parametrize_maze_files(classic_mazes)
halfsize_mazes = parametrize_maze_files(halfsize_mazes)
training_mazes = parametrize_maze_files(training_mazes)
competition_mazes = parametrize_maze_files(competition_mazes)
all_mazes = parametrize_maze_files(all_mazes)


def read_maze(maze_file):
    rows = maze_file.read_text().split('\n')
    for i, row in enumerate(rows):
        if not row.startswith(('o', '|')):
            break
    return rows[:i]


def find_tagged_cells(rows, tag):
    """
    Find the set of cell positions that have a given tag.
    """
    found = set()
    for i, row in enumerate(reversed(rows[1::2])):
        for j, column in enumerate(row[2::4]):
            if column is tag:
                found.add((i, j))
    return found


@all_mazes
def test_file_name(maze_file):
    """
    - All maze files must be text files with `.txt` extension.
    - Only "a-z", "0-9" and "-" characters are allowed.
    """
    assert maze_file.suffix == '.txt'
    assert re.match(r'^[a-z0-9\-]*$', maze_file.stem)


@classic_mazes
def test_classic_size(maze_file):
    """
    Classic maze size is always 16x16.
    """
    rows = read_maze(maze_file)
    assert len(rows) == (CLASSIC_SIZE * 2 + 1)
    assert all(len(row) == (CLASSIC_SIZE * 4 + 1) for row in rows)


@training_mazes
def test_training_size(maze_file):
    """
    Training maze size is the same as classic size, even if not fully used.
    """
    rows = read_maze(maze_file)
    assert len(rows) == (CLASSIC_SIZE * 2 + 1)
    assert all(len(row) == (CLASSIC_SIZE * 4 + 1) for row in rows)


@all_mazes
def test_format(maze_file):
    """
    Maze file format must be homogeneous. Vertical walls are represented with
    a `|`, horizontal walls with `---` and posts with `o`.

    Even rows must:

    - Have a post each 4 characters.
    - Have a wall `---` or nothing `   ` between posts.

    Odd rows must:

    - Have a wall `|` or nothing ` ` each 4 characters.
    """
    rows = read_maze(maze_file)
    even_rows = rows[::2]
    assert all(all(x == 'o' for x in row[::4]) for row in even_rows)
    assert all(all(x in ('---', '   ') for x in row.strip('o').split('o'))
               for row in even_rows)
    odd_rows = rows[1::2]
    assert all(all(x in ('|', ' ') for x in row[::4]) for row in odd_rows)


@all_mazes
def test_boundaries(maze_file):
    """
    Maze boundaries are expected to be closed.
    """
    rows = read_maze(maze_file)
    east_boundary = [row[-1] for row in rows[1::2]]
    west_boundary = [row[0] for row in rows[1::2]]
    assert all(v == '|' for v in east_boundary + west_boundary)
    north_boundary = rows[0].strip('o').split('o')
    south_boundary = rows[-1].strip('o').split('o')
    assert all(h == '---' for h in north_boundary + south_boundary)


@all_mazes
def test_starting_cell_unique(maze_file):
    """
    The starting cell, if marked, must be unique.
    """
    rows = read_maze(maze_file)
    assert Counter(''.join(rows))['S'] in (0, 1)


@competition_mazes
def test_starting_cell(maze_file):
    """
    The starting cell is expected to be at the South-West and facing North.
    """
    rows = read_maze(maze_file)
    assert rows[-3][:5] == 'o   o'
    assert rows[-2][:5] == '| S |'
    assert rows[-1][:5] == 'o---o'


@competition_mazes
def test_goal_cells(maze_file):
    """
    Goal cells must be marked with a "G" and form a rectangular area.
    """
    rows = read_maze(maze_file)
    goals = find_tagged_cells(rows, 'G')
    assert len(goals) >= 1
    x = [cell[0] for cell in list(goals)]
    y = [cell[1] for cell in list(goals)]
    rangex = range(min(x), max(x) + 1)
    rangey = range(min(y), max(y) + 1)
    assert goals == set(product(rangex, rangey))


@classic_mazes
def test_classic_goal_cells(maze_file):
    """
    Classic goal cells are always in the middle of the maze.
    """
    rows = read_maze(maze_file)
    goals = find_tagged_cells(rows, 'G')
    assert goals == {(7, 7), (7, 8), (8, 7), (8, 8)}
