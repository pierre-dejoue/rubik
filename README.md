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
