Algorithm Finder for the 2x2x2 Rubik's Cube
===========================================

![Python3](http://img.shields.io/badge/python-3.13-blue.svg?v=1)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](./LICENSE)

## Usage

```
$ python rubik2x2.py --help
usage: rubik2x2.py [-h] [--doc] [--show-colors] [--solve] [--max MAX] [--maxmax] [-c CUBE] [-p PIVOT_CORNER] [-a ALGORITHM]

Find algorithms for the 2x2x2 Rubik's cube.

options:
  -h, --help            show this help message and exit
  --doc                 Additional documentation
  --show-colors         Show the association of faces to colors then exit
  --solve               Solve the cube from the position defined with -c/--cube
  --max MAX             Max search depth. (Default: 10)
  --maxmax              Always go to max search depth
  -c, --cube CUBE       A configuration of the cube. Read the doc with --doc.
  -p, --pivot PIVOT_CORNER
                        The pivot corner is to remain fixed. (Default: LDB)
  -a, --algo ALGORITHM  Apply an algorithm to the cube. For example: "R U2 R'"

```

## Tutorial

### Notations

#### Move Notation

We're using the standard convention to name the cube faces and rotations. Those are sometimes refered to as the Singmaster notations. We provide a quick summary below:

The six faces of the Rubik's cube are named:

```
L: Left
R: Right
U: Up
D: Down
F: Front
B: Back
```

The following pairs of faces are aligned along the 3D axis:

```
L/R: X axis
U/D: Y axis
F/B: Z axis
```

The name of each face is also used to designate a clockwise quarter rotation of that face of the cube. The schema below illustrates this:

![Rubik's cube move notation](doc/img/cube_rotations_2x2x2_xyz.png)

This schema is adapted from the content of website [myrubik.com](https://myrubik.com/), shared under [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) license.

Read more about the move Singmaster notation of the Rubik's cube on [myrubik.com -- The 2x2x2 cube pieces and notation](https://myrubik.com/en/notation/2x2x2), and [rubiks.fandom.com -- Notation](https://rubiks.fandom.com/wiki/Notation)

#### Static Notation

The script is using a custom notation to capture any position of the 2x2 cube (including [illegal positions not reachable from the solved state](https://www.speedcubing.com/chris/legal.html))

That notation is documented [in details here](./doc/cube_static_notation.md), and below is a quick reference sheet:

- The position of the corners is the following:

![static position notation: Corner position](doc/img/cube_positions.png)

- The orientation of the corners is shown below. We represent with a star ( * ) the face of the corner that is up (U) or down (D) in the solved state. With the Western color scheme, the * face is either the white or the yellow one.

![static position notation: Corner orientation](doc/img/cube_orientations.png)

## Color Scheme

An optional `config.ini` can be provided to set a color scheme.

Examples of config files are given for the most common color schemes: [./config/config_japanese.ini](./config/config_japanese.ini),  [./config/config_western.ini](./config/config_western.ini)

Option `--show-colors` of the script prints out the current color scheme:

```
$ python rubik2x2.py --show-colors

Faces:
    R: red
    L: orange
    U: white
    D: yellow
    F: green
    B: blue

Corners:
    0 (LDB): orange-yellow-blue
    1 (RDB): red-yellow-blue
    2 (RUB): red-white-blue
    3 (LUB): orange-white-blue
    4 (LDF): orange-yellow-green
    5 (RDF): red-yellow-green
    6 (RUF): red-white-green
    7 (LUF): orange-white-green
```

## Maintenance

### Requirements

* __Python 3.x__: http://www.python.org/download/

No `requirements.txt` at the moment.

### Unit Tests

```
python -m unittest -v
```

### Static Checks

```
pylint  $(git ls-files '*.py')
ruff check
mypy .
```

## God's number

To this repo we annexed a C++ program that finds the [God's number](https://en.wikipedia.org/wiki/God%27s_algorithm) of the 2x2x2 Rubik's cube.

Please read: [cpp/README.md](cpp/README.md)

The convention used to describe a transformation of the cube (position and orientation of the corners) in the C++ project is the same as in the Python script.
