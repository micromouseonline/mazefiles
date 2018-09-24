**Please refer to the issues where a proposed file format change is described**

# mazefiles
A set of micromouse maze files in text format. They have been collected over some years from many sources.

These files are a companion to the maze tool https://github.com/micromouseonline/micromouse_maze_tool.

The format used here is as follows:

- All posts are represented with the character `o`.
- All posts must be present in the grid even if there is no wall attached to
  them.
- Horizontal walls are represented with three `---`.
- Vertical walls are represented with a single `|`.
- The goal cells are marked with a `G` in the certer of the cell.
- The starting cell is marked with an `S` in the certer of the cell.

Here is an example of a 4x4 maze:

```
o---o---o---o---o
| G |           |
o   o   o   o---o
|       |       |
o---o---o---o   o
|               |
o   o---o---o   o
| S |           |
o---o---o---o---o
```

**classic** mazes are all 16x16. Some of these have smaller active areaswhere the event in which they were used only had a smaller maze available. That may have been 7x8, 8x8, 11x11 or some other size. All these mazes have a legal goal cell in cell 7,7.

**halfsize** mazes are all 32x32. The goal is not fixed in the same way as it might be in the classic contest. The goal for halfsize mazes is a single cell, marked with a "G" in the center of the cell, which may be part of a larger area.

**training** mazes are all 16x16 but may not have legal goal areas as the useable area might be only 5x5, 8x8, 10x5 or some other size representing small mazes used for testing a mouse where there is not room for a full sized maze. The filename should indicate the active area.

The files may, or may not, represent actual contest mazes. If there are errors in contest mazes, please let me know. Preferably with a photo of the original maze so that I can make changes.


## FAQ

### How can I contribute to the repository?

Thanks for your interest! Start by reading GitHub's guide on [how to propose
changes to someone else's project][0], then feel free to create a pull request
with your changes or new maze files.

### Why text files?

- They are easy to understand by humans.
- They get along with version control systems (Git).
- They are easy to read/write with any programming language.
- They are easy to visualize (just use your browser or favorite text editor).
- No need for special tools if you want to edit them or create your own. Just
  a bit of patience is required.

### Are there any tools to help me create maze files?

- If you happen to have an image of a micromouse maze setup you might want to
  try the [Optical Micromouse Maze Recognition software][1].


[0]: https://help.github.com/articles/fork-a-repo/
[1]: https://github.com/Theseus/ommr
