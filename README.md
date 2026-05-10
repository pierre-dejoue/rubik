Algorithm Finder for the 2x2x2 Rubik's Cube
===========================================

![Python3](http://img.shields.io/badge/python-3.13-blue.svg?v=1)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](./LICENSE)

## Usage

```
$ python rubik2x2.py -h
usage: rubik2x2.py [-h] [--doc] [--max MAX] [--maxmax] [-c CUBE] [-p PIVOT_CORNER] [-a ALGORITHM]

Find algorithms for the 2x2x2 Rubik's cube. License: MIT License

options:
  -h, --help            show this help message and exit
  --doc                 Additional documentation
  --max MAX             Max search depth
  --maxmax              Go to max search depth.
  -c, --cube CUBE       A configuration of the cube
  -p, --pivot PIVOT_CORNER
                        Pivot corner. Default=LDB
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

The script is using a custom notation to capture any position of the cube (including [illegal positions not reachable from the solved state](https://www.speedcubing.com/chris/legal.html))

This notation is documented [here](./doc/cube_static_notation.md).


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
