#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find formulas for the 2x2x2 Rubik's cube
"""

from functools import reduce
import argparse
import copy
import re
import sys


def error(msg):
    print('Error: ' + msg, file = sys.stderr)
    exit(-1)


class CornerPosition:
    """Corner position"""

    @staticmethod
    def is_valid_str(corner):
        return re.match('^(L|R)(D|U)(B|F)$', corner) is not None

    @staticmethod
    def from_str(corner):
        assert CornerPosition.is_valid_str(corner)
        pos = {
            'LDB': 0,
            'RDB': 1,
            'RUB': 2,
            'LUB': 3,
            'LDF': 4,
            'RDF': 5,
            'RUF': 6,
            'LUF': 7,
        }.get(corner.upper(), 0)
        return pos


class CornerOrientation:
    """CornerOrientation"""

    @staticmethod
    def rotate(orientation, rotation):
        return (orientation + rotation) % 3


class Cube:
    """Uniquely defines a configuration of the 2x2x2 cube.

    Holds the permutation of the 8 corners and their orientation.

    For instance:

      31270564;20011002

    is the configuration of the solved cube to which a L rotation
    has been applied.
    """

    sep = ':'

    def __init__(self, permutation: list, orientations: list):
        assert len(permutation) == 8
        assert set(permutation) == set(range(8))
        assert len(orientations) == 8
        self.permutation = permutation
        self.orientations = orientations

    def __repr__(self):
        return ''.join(map(str, self.permutation)) + self.sep + ''.join(map(str, self.orientations))

    def __iter__(self):
        return zip(self.permutation, self.orientations)

    def orientation(self):
        return reduce(CornerOrientation.rotate, self.orientations, 0)

    def is_solvable(self, pivot):
        idx = CornerPosition.from_str(pivot)
        pivot_is_fixed = self.permutation[idx] == idx and self.orientations[idx] == 0
        orientation_is_zero = self.orientation() == 0
        return pivot_is_fixed and orientation_is_zero

    def __eq__(self, other):
        return self.permutation == other.permutation and self.orientations == other.orientations

    def __ne__(self, other):
        return not self == other

    @classmethod
    def from_str(cls, cube_str: str):
        lists = cube_str.split(cls.sep)
        assert len(lists) == 2
        perm = list(map(int, list(lists[0])))
        orient = list(map(int, list(lists[1])))
        return cls(perm, orient)

    @classmethod
    def solved(cls):
        return cls([0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0])


#
# Combine position + orientation to define all rotations on the cube
#
# As a convention (and to get rid of the symetries of the cube) we fix
# the first corner in space (i.e. corner 0 is assumed to be already in
# the 'solved' position.)
# This means that we can limit the scope to only one rotation per axis,
# namely a quarter turn on the face opposite to the fixed corner.
#
class Rot:
    def __init__(self, permutation: list, orientations: list, axis: str, name: str):
        self.cube = Cube(permutation, orientations)
        self.axis = axis.upper()
        assert self.axis in ['X', 'Y', 'Z']
        self.name = name

    def is_valid(self):
        return self.cube.orientation() == 0

    def apply(self, cube: Cube) -> Cube:
        permutation = [self.cube.permutation[i] for i in cube.permutation]
        orientations = [CornerOrientation.rotate(o, self.cube.orientations[i]) for (i, o) in cube]
        return Cube(permutation, orientations)

    def to_string(self, nb_of_quarter_turns = 1):
        if nb_of_quarter_turns % 4 == 1:
            return self.name
        elif nb_of_quarter_turns % 4 == 2:
            return self.name + '2'
        elif nb_of_quarter_turns % 4 == 3:
            return self.name + '\''
        else:
            return "I"      # No rotation

    def __repr__(self):
        return self.to_string()


class Rotation:
    """Basic rotations

    Prime (e.g. L') :

    Rotation along the X axis:
    L = clockwise quarter turn rotation on the "left" face
    R = clockwise quarter turn rotation on the "right" face

    Rotation along the Y axis:
    D = clockwise quarter turn rotation on the "down" face
    U = clockwise quarter turn rotation on the "up" face

    Rotation along the Z axis:
    B = clockwise quarter turn rotation on the "back" face
    F = clockwise quarter turn rotation on the "front" face

    Suffix:
    Prime, e.g. L' = counter clockwise quarter turn
    Square, e.g. L2 = half turn

    Reorientation of the cube:
    X = L' R
    Y = D' U
    Z = B' F
    """
    L = Rot([3, 1, 2, 7, 0, 5, 6, 4], [2, 0, 0, 1, 1, 0, 0, 2], 'X', 'L')
    R = Rot([0, 5, 1, 3, 4, 6, 2, 7], [0, 1, 2, 0, 0, 2, 1, 0], 'X', 'R')

    D = Rot([4, 0, 2, 3, 5, 1, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0], 'Y', 'D')
    U = Rot([0, 1, 6, 2, 4, 5, 7, 3], [0, 0, 0, 0, 0, 0, 0, 0], 'Y', 'U')

    B = Rot([1, 2, 3, 0, 4, 5, 6, 7], [1, 2, 1, 2, 0, 0, 0, 0], 'Z', 'B')
    F = Rot([0, 1, 2, 3, 7, 4, 5, 6], [0, 0, 0, 0, 2, 1, 2, 1], 'Z', 'F')

    X = Rot([4, 5, 1, 0, 7, 6, 2, 3], [2, 1, 2, 1, 1, 2, 1, 2], 'X', 'X')
    Y = Rot([1, 5, 6, 2, 0, 4, 7, 3], [0, 0, 0, 0, 0, 0, 0, 0], 'Y', 'Y')
    Z = Rot([3, 0, 1, 2, 7, 4, 5, 6], [1, 2, 1, 2, 2, 1, 2, 1], 'Z', 'Z')

    All = {r.name: r for r in [L, R, D, U, B, F, X, Y, Z]}

    @staticmethod
    def from_str(rot: str):
        assert rot
        cw_quarter_turns = 1
        if rot[-1] == '2':
            rot = rot[:-1]
            cw_quarter_turns = 2
        elif rot[-1] == '\'':
            rot = rot[:-1]
            cw_quarter_turns = 3
        if rot not in Rotation.All:
            raise Exception('Rotation not found [%s]' % rot)
        return Rotation.All[rot], cw_quarter_turns

class Algorithm:
    """An algorithm is a list of rotations applied to the cube"""

    def __init__(self):
        self.rotations = []
        self.clockwise_quarter_turns = []

    def append(self, rotation: Rot, clockwise_quarter_turns: int):
        assert clockwise_quarter_turns % 4 != 0
        self.rotations.append(rotation)
        self.clockwise_quarter_turns.append(clockwise_quarter_turns % 4)

    def apply(self, cube: Cube = Cube.solved()) -> Cube:
        result_cube = copy.deepcopy(cube)
        for (r, n) in self:
            for _ in range(n):
                result_cube = r.apply(result_cube)
        return result_cube

    def __len__(self):
        assert len(self.rotations) == len(self.clockwise_quarter_turns)
        return len(self.rotations)

    def __iter__(self):
        return zip(self.rotations, self.clockwise_quarter_turns)

    def __repr__(self):
        rotations_str = [r.to_string(n) for (r, n) in self]
        return ' '.join(rotations_str)

    def __copy__(self):
        new_algo = type(self)()
        new_algo.rotations = self.rotations.copy()
        new_algo.clockwise_quarter_turns = self.clockwise_quarter_turns.copy()
        return new_algo

    @classmethod
    def from_str(cls, algo: str):
        result = cls()
        for rot in algo.split():
            r, n = Rotation.from_str(rot)
            result.append(r, n)
        return result


def rotations_from_pivot(pivot: str):
    assert CornerPosition.is_valid_str(pivot)
    rotations = []
    rotations.append(Rotation.R if 'L' in pivot else Rotation.L)
    rotations.append(Rotation.U if 'D' in pivot else Rotation.D)
    rotations.append(Rotation.F if 'B' in pivot else Rotation.B)
    return rotations


class ExploreSolutions:
    def __init__(self, allowed_rotations, result_found_predicate, on_result_found):
        self.allowed_rotations = allowed_rotations
        self.result_found_predicate = result_found_predicate
        self.on_result_found = on_result_found

    # - Do not rotate on the same axis as the caller
    # - Check clockwise, counter-clockwise, half-turn on the two remaining axis
    def recurse_exploration(self, max_depth, state: Cube = Cube.solved(), previous_rots: Algorithm = Algorithm()):
        found = False
        for rot in self.allowed_rotations:
            if len(previous_rots) > 0 and previous_rots.rotations[-1].axis == rot.axis:
                continue
            new_state = state
            for n in range(3):
                new_state = rot.apply(new_state)
                new_rots = copy.copy(previous_rots)
                new_rots.append(rot, n + 1)
                if (self.result_found_predicate(new_state)):
                    self.on_result_found(new_state, new_rots)
                    found = True
                elif len(new_rots) < max_depth:
                    found = found | self.recurse_exploration(max_depth, new_state, new_rots)
        return found


def funny_tip(depth):
    return {
        7: 'Not just yet!',
        9: 'Go make a coffee...',
        10: 'Go watch a movie!',
        11: 'The end of the Universe is nigh',
    }.get(depth, '')


#
# Main
#
def main():
    parser = argparse.ArgumentParser(description='Explore the 2x2x2 Rubik\'s cube')
    parser.add_argument('--max', dest='max', type=int, help='Max search depth', required=False, default=8)
    parser.add_argument('-c', '--cube', dest='target_cube',  help='Target configuration of the cube', required=False, default = str(Cube.solved()))
    default_pivot = 'LDB'
    parser.add_argument('-p', '--pivot', dest='pivot_corner', help='Pivot corner. Default=' + default_pivot, required=False, default = default_pivot)
    parser.add_argument('-a', '--algo', dest='algorithm', help='An algorithm. For example: R U2 R\'', required=False, default = None)
    args = parser.parse_args()

    if args.algorithm is not None:
        algo = Algorithm.from_str(args.algorithm)
        print(algo.apply())
        return

    target_cube = Cube.from_str(args.target_cube)
    pivot = args.pivot_corner

    if not CornerPosition.is_valid_str(pivot):
        error('Invalid pivot [%s]. Pivot must follow this format: (L|R)(D|U)(B|F)' % pivot)
    if not target_cube.is_solvable(pivot):
        error('The target position [%s] cannot be obtained with pivot %s (%d)' % (target_cube, pivot, CornerPosition.from_str(pivot)))

    allowed_rotations = rotations_from_pivot(args.pivot_corner)

    def found_predicate(cube: Cube):
        return cube == target_cube

    def process_solution(state: Cube, rotations: Algorithm):
        print('%s %d [ %s ]' % (state, len(rotations), str(rotations)), flush=True)

    explore_solutions = ExploreSolutions(allowed_rotations, found_predicate, process_solution)
    found = False
    depth = 1
    while not found and depth <= args.max:
        print('Recurse depth: %d %s' % (depth, funny_tip(depth)), flush=True)
        found = explore_solutions.recurse_exploration(depth)
        depth = depth + 1


if __name__ == "__main__":
    main()
