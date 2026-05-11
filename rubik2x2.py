#!/usr/bin/env python
"""
Find algorithms for the 2x2x2 Rubik's cube.

License:
    MIT License
"""
import argparse
import configparser
import copy
import re
import sys
from functools import reduce
from types import SimpleNamespace


DEFAULT_CONFIG_FILE = 'config.ini'

ADDITIONAL_DOCUMENTATION = './doc/cube_static_notation.md'

ALL_FACES = ['R', 'L', 'U', 'D', 'F', 'B']

CORNERS_IN_ORDER = [
    'LDB',
    'RDB',
    'RUB',
    'LUB',
    'LDF',
    'RDF',
    'RUF',
    'LUF',
]

config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG_FILE)

def error_and_exit(msg):
    print('Error: ' + msg, file=sys.stderr)
    sys.exit(-1)


class CornerPosition:
    """Corner position

    The positions are defined as follows:

    Back layer (B):

      3   2

      0   1

    Front layer (F):

      7   6

      4   5

    """

    default_pivot = 'LDB'       # position: 0

    @staticmethod
    def is_valid_string(corner: str) -> bool:
        return re.match('^(L|R)(D|U)(B|F)$', corner) is not None

    @staticmethod
    def from_string(corner: str) -> int:
        assert CornerPosition.is_valid_string(corner)
        pos = CORNERS_IN_ORDER.index(corner.upper())
        return pos

    @staticmethod
    def to_string(pos: int):
        assert pos >= 0 and pos < 8
        return CORNERS_IN_ORDER[pos]


class CornerOrientation:
    """CornerOrientation

    There are three possible orientations of a corner. To explain the naming convention,
    let's first observe that every corner has a colored face that is either down (D),
    or up (U) when the cube is in the solved state. Let's call that unique face the star
    face of the corner (*).

      0: The star face is either up or down (it is aligned with the XZ plane)
      1: clockwise rotation from the 0 orientation
      2: counterclockwise rotation from the 0 orientation
    """

    @staticmethod
    def rotate(orientation, rotation):
        return (orientation + rotation) % 3


class Cube:
    """Uniquely define a configuration of the 2x2x2 cube.

    Holds the permutation of the 8 corners and their orientation.

    For instance:

      31270564:20011002

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
        idx = CornerPosition.from_string(pivot)
        pivot_is_fixed = self.permutation[idx] == idx and self.orientations[idx] == 0
        orientation_is_zero = self.orientation() == 0
        return pivot_is_fixed and orientation_is_zero

    def fixed_corners(self):
        fixed_position = []
        fixed_position_n_orientation = []
        for idx in range(8):
            if self.permutation[idx] == idx:
                if self.orientations[idx] != 0:
                    fixed_position.append(idx)
                else:
                    fixed_position_n_orientation.append(idx)
        return fixed_position, fixed_position_n_orientation

    def __eq__(self, other):
        return self.permutation == other.permutation and self.orientations == other.orientations

    def __ne__(self, other):
        return not self == other

    @classmethod
    def is_valid_string(cls, cube_str: str) -> bool:
        lists = cube_str.split(cls.sep)
        if len(lists) != 2:
            return False
        if len(lists[0]) != 8 or set(lists[0]) != set('01234567'):
            return False
        if len(lists[1]) != 8 or len(set(lists[1]) - set('012')) != 0:
            return False
        return True

    @classmethod
    def from_string(cls, cube_str: str) -> 'Cube':
        assert cls.is_valid_string(cube_str)
        lists = cube_str.split(cls.sep)
        perm = list(map(int, list(lists[0])))
        orient = list(map(int, list(lists[1])))
        return cls(perm, orient)

    @classmethod
    def solved(cls) -> 'Cube':
        return cls([0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0])


class CubePattern:
    """Pattern that represents a family of cube transformations"""

    sep = Cube.sep
    wildcard = '*'

    def __init__(self, permutation: list, orientations: list):
        assert len(permutation) == 8
        assert len(orientations) == 8
        self.permutation = permutation
        self.orientations = orientations

    def __repr__(self):
        return ''.join(self.permutation) + self.sep + ''.join(self.orientations)

    def match(self, cube: Cube):
        match_perm = all(pattern == self.wildcard or pattern == str(perm)
                            for (perm, pattern) in zip(cube.permutation, self.permutation))
        match_orient = all(pattern == self.wildcard or pattern == str(orient)
                            for (orient, pattern) in zip(cube.orientations, self.orientations))
        return match_perm and match_orient

    def is_cube(self):
        return self.wildcard not in self.permutation and self.wildcard not in self.orientations

    def to_cube(self) -> Cube:
        assert self.is_cube()
        return Cube(list(map(int, self.permutation)), list(map(int, self.orientations)))

    def check_parity(self) -> bool:
        if self.wildcard in self.orientations:
            return True
        return self.to_cube().orientation() == 0

    def is_solvable(self, pivot):
        if self.is_cube():
            return self.to_cube().is_solvable(pivot)
        idx = CornerPosition.from_string(pivot)
        pivot_is_fixed = (self.permutation[idx] in [str(idx), self.wildcard] and
                          self.orientations[idx] in ['0', self.wildcard])
        return pivot_is_fixed

    @classmethod
    def is_valid_string(cls, pattern_str: str) -> bool:
        lists = pattern_str.split(cls.sep)
        if len(lists) != 2:
            return False
        if len(lists[0]) != 8 or len(set(lists[0]) - set('01234567' + cls.wildcard)) != 0:
            return False
        if len(lists[1]) != 8 or len(set(lists[1]) - set('012' + cls.wildcard)) != 0:
            return False
        return True

    @classmethod
    def from_string(cls, pattern_str: str) -> 'CubePattern':
        assert cls.is_valid_string(pattern_str)
        lists = pattern_str.split(cls.sep)
        perm =  list(lists[0])
        orient = list(lists[1])
        return cls(perm, orient)


class Rot:
    """Combine the position and orientation of all corners to define a rotation of the cube"""

    def __init__(self, cube: Cube, axis: str, name: str):
        self.cube = cube
        self.axis = axis.upper()
        assert self.axis in ['X', 'Y', 'Z']
        self.name = name

    @classmethod
    def from_perm(cls, permutation: list, orientations: list, axis: str, name: str) -> 'Rot':
        return cls(Cube(permutation, orientations), axis, name)

    @classmethod
    def identity(cls) -> 'Rot':
        return cls(Cube.solved(), 'X', 'I')

    def is_valid(self) -> bool:
        return self.cube.orientation() == 0

    def apply(self, cube: Cube) -> Cube:
        """Apply this rotation to the cube"""
        permutation = [self.cube.permutation[p] for p in cube.permutation]
        orientations = [CornerOrientation.rotate(o, self.cube.orientations[p]) for (p, o) in cube]
        return Cube(permutation, orientations)

    def __repr__(self):
        return self.name


#
# Name and list all clockwise quarter rotations
#
CWQuarterRot = SimpleNamespace(
    L = Rot.from_perm([3, 1, 2, 7, 0, 5, 6, 4], [2, 0, 0, 1, 1, 0, 0, 2], 'X', 'L'),
    R = Rot.from_perm([0, 5, 1, 3, 4, 6, 2, 7], [0, 1, 2, 0, 0, 2, 1, 0], 'X', 'R'),
    D = Rot.from_perm([4, 0, 2, 3, 5, 1, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0], 'Y', 'D'),
    U = Rot.from_perm([0, 1, 6, 2, 4, 5, 7, 3], [0, 0, 0, 0, 0, 0, 0, 0], 'Y', 'U'),
    B = Rot.from_perm([1, 2, 3, 0, 4, 5, 6, 7], [1, 2, 1, 2, 0, 0, 0, 0], 'Z', 'B'),
    F = Rot.from_perm([0, 1, 2, 3, 7, 4, 5, 6], [0, 0, 0, 0, 2, 1, 2, 1], 'Z', 'F'),
    X = Rot.from_perm([4, 5, 1, 0, 7, 6, 2, 3], [2, 1, 2, 1, 1, 2, 1, 2], 'X', 'X'),
    Y = Rot.from_perm([1, 5, 6, 2, 0, 4, 7, 3], [0, 0, 0, 0, 0, 0, 0, 0], 'Y', 'Y'),
    Z = Rot.from_perm([3, 0, 1, 2, 7, 4, 5, 6], [1, 2, 1, 2, 2, 1, 2, 1], 'Z', 'Z'),
)
all_cw_quarter_rotations = {r.name: r for r in [
        CWQuarterRot.L,
        CWQuarterRot.R,
        CWQuarterRot.D,
        CWQuarterRot.U,
        CWQuarterRot.B,
        CWQuarterRot.F,
        CWQuarterRot.X,
        CWQuarterRot.Y,
        CWQuarterRot.Z,
    ]}


def cw_quarter_rotation_to_string(cw_quarter_rot: Rot, nb_of_quarter_turns: int = 1) -> str:
    name = cw_quarter_rot.name
    assert name in all_cw_quarter_rotations
    if nb_of_quarter_turns % 4 == 1:
        return name
    if nb_of_quarter_turns % 4 == 2:
        return f'{name}2'
    if nb_of_quarter_turns % 4 == 3:
        return f'{name}\''
    assert nb_of_quarter_turns % 4 == 0
    return 'I'  # No rotation (This is the identity transformation)


class RepeatRot:
    """A repeated rotation. E.g. L2, R, D'"""

    def __init__(self, rot: Rot, repeat: int = 1):
        assert repeat >= 0
        self.rot = rot
        self.repeat = repeat

    def __repr__(self):
        if self.repeat == 0:
            return 'I'
        if self.repeat == 1:
            return self.rot.name
        return f'{self.rot.name}{self.repeat}'

    def __str__(self):
        if self.rot.name in all_cw_quarter_rotations:
            return cw_quarter_rotation_to_string(self.rot, self.repeat)
        return self.__repr__()

    @classmethod
    def identity(cls) -> 'RepeatRot':
        return cls(Rot.identity(), 0)

    @classmethod
    def from_string(cls, rot_str: str) -> 'RepeatRot':
        """Rotations

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
        Prime, e.g. L' = counterclockwise quarter turn
        Square, e.g. L2 = half turn
        Cube, e.g. L3 = L' (This is non standard, but supported by this script)

        Reorientation of the cube:
        X = L' R
        Y = D' U
        Z = B' F
        """
        assert len(rot_str) == 1 or len(rot_str) == 2
        if rot_str == 'I':
            return cls.identity()
        cw_quarter_turns = 1
        if rot_str[-1] == '2':
            rot_str = rot_str[:-1]
            cw_quarter_turns = 2
        elif rot_str[-1] == '\'' or rot_str[-1] == '3':
            rot_str = rot_str[:-1]
            cw_quarter_turns = 3
        assert len(rot_str) == 1
        if rot_str not in all_cw_quarter_rotations:
            raise RuntimeError(f'Rotation not found [{rot_str}]')
        return cls(all_cw_quarter_rotations[rot_str], cw_quarter_turns)


class Algorithm:
    """An algorithm is a list of rotations applied to the cube"""

    def __init__(self):
        self.rotations = []

    def append(self, rotation: RepeatRot):
        if rotation.repeat > 0:
            self.rotations.append(rotation)

    def apply(self, cube: Cube = Cube.solved()) -> Cube:
        result_cube = copy.deepcopy(cube)
        for rr in self.rotations:
            for _ in range(rr.repeat):
                result_cube = rr.rot.apply(result_cube)
        return result_cube

    def cyclic_order(self):
        order = 0
        cube = Cube.solved()
        while True:
            order = order + 1
            cube = self.apply(cube)
            if cube == Cube.solved():
                break
        return order

    def __len__(self):
        return len(self.rotations)

    def __repr__(self):
        rotations_str = [repr(rr) for rr in self.rotations]
        return ' '.join(rotations_str)

    def __str__(self):
        rotations_str = [str(rr) for rr in self.rotations]
        return ' '.join(rotations_str)

    def __copy__(self):
        new_algo = type(self)()
        new_algo.rotations = self.rotations.copy()
        return new_algo

    @classmethod
    def from_string(cls, algo: str):
        result = cls()
        for rot in algo.split():
            r = RepeatRot.from_string(rot)
            result.append(r)
        return result


def rotations_from_pivot(pivot: str):
    """List the allowed base rotations for this pivot corner

    E.g. if the pivot is LUF, then only the rotations R, D and B can be used
    """
    assert CornerPosition.is_valid_string(pivot)
    rotations = []
    rotations.append(CWQuarterRot.R if 'L' in pivot else CWQuarterRot.L)
    rotations.append(CWQuarterRot.U if 'D' in pivot else CWQuarterRot.D)
    rotations.append(CWQuarterRot.F if 'B' in pivot else CWQuarterRot.B)
    return rotations


class ExploreSolutions:
    """Recursively explore the graph of the cube configurations

    The search is DFS to not explode the RAM consumption, with a cap on the maximum search depth.

    When incrementing the search depth (by adding a new rotation to the algorithm):
     - Do not rotate on the same axis as the caller
     - Check clockwise, counter-clockwise, half-turn on the two remaining axis
    """
    def __init__(self, allowed_rotations, result_found_predicate, on_result_found):
        self.allowed_rotations = allowed_rotations
        self.result_found_predicate = result_found_predicate
        self.on_result_found = on_result_found

    def recursive_dfs_exploration(self, max_depth, state: Cube = Cube.solved(), previous_rots: Algorithm = Algorithm()):
        found = False
        for rot in self.allowed_rotations:
            if len(previous_rots) > 0 and previous_rots.rotations[-1].rot.axis == rot.axis:
                continue
            new_state = state
            for repeat in range(1, 4):
                new_state = rot.apply(new_state)
                new_rots = copy.copy(previous_rots)
                new_rots.append(RepeatRot(rot, repeat))
                if self.result_found_predicate(new_state):
                    self.on_result_found(new_state, new_rots)
                    found = True
                elif len(new_rots) < max_depth:
                    found = found | self.recursive_dfs_exploration(max_depth, new_state, new_rots)
        return found


def funny_hint(depth: int) -> str:
    return {
        7: 'Not just yet!',
        9: 'Go make a coffee...',
        10: 'Go watch a movie!',
        11: 'The end of the Universe is nigh',
    }.get(depth, '')


def get_face_colors_from_config() -> dict[str, str]:
    colors = {}
    colors['R'] = config.get('colors', 'face_R', fallback='')
    colors['L'] = config.get('colors', 'face_L', fallback='')
    colors['U'] = config.get('colors', 'face_U', fallback='')
    colors['D'] = config.get('colors', 'face_D', fallback='')
    colors['F'] = config.get('colors', 'face_F', fallback='')
    colors['B'] = config.get('colors', 'face_B', fallback='')
    if not all(colors.values()) or len(set(colors.values())) != 6:
        return {}
    return colors


def corner_to_colors(corner: str, colors: dict[str, str]):
    assert CornerPosition.is_valid_string(corner)
    return f'{colors[corner[0]]}-{colors[corner[1]]}-{colors[corner[2]]}'


#
# Main
#
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--doc', dest='documentation', action='store_true',
                        help='Additional documentation')
    parser.add_argument('--show-colors', dest='show_colors', action='store_true',
                        help='Show the association of faces to colors then exit')
    parser.add_argument('--max', dest='max', type=int, required=False, default=10,
                        help='Max search depth')
    parser.add_argument('--maxmax', dest='goto_max_depth', action='store_true',
                        help='Go to max search depth.')
    parser.add_argument('-c', '--cube', dest='cube', required=False, default=str(Cube.solved()),
                        help='A configuration of the cube')
    parser.add_argument('-p', '--pivot', dest='pivot_corner', required=False, default=CornerPosition.default_pivot,
                        help=f'The pivot corner is to remain fixed. Default={CornerPosition.default_pivot}')
    parser.add_argument('-a', '--algo', dest='algorithm', required=False, default=None,
                        help='Apply an algorithm to the cube. For example: "R U2 R\'"')
    args = parser.parse_args()

    indent = 4*' '
    if args.documentation:
        try:
            doc_filepath = ADDITIONAL_DOCUMENTATION
            with open(doc_filepath, 'r') as fp:
                print('\n')
                for line in fp:
                    print(f'{indent}{line.strip()}')
                print('\n')
        except FileNotFoundError:
            error_and_exit(f'The documentation file was not found: {doc_filepath}')
        return

    face_colors = get_face_colors_from_config()
    if args.show_colors:
        if face_colors:
            print()
            print('Faces:')
            for face in ALL_FACES:
                print(f'{indent}{face}: {face_colors[face]}')
            print()
            print('Corners:')
            for idx, corner in enumerate(CORNERS_IN_ORDER):
                print(f'{indent}{idx} ({corner}): {corner_to_colors(corner, face_colors)}')
        else:
            print(f'No color configuration found, check {DEFAULT_CONFIG_FILE}')
        return

    if args.algorithm is not None:      # Empty string: The transformation is the identity
        algo = Algorithm.from_string(args.algorithm)
        starting_cube = Cube.from_string(args.cube)
        cube = algo.apply(starting_cube)
        print(cube)
        fixed_corners = ['-'] * 8
        fixed_position, fixed_position_n_orientation = cube.fixed_corners()
        for idx in fixed_position:
            fixed_corners[idx] = '~'
        for idx in fixed_position_n_orientation:
            fixed_corners[idx] = '+'
        print(''.join(fixed_corners))
        print(f'cyclic_order: {algo.cyclic_order()}')
        return

    target_pattern = CubePattern.from_string(args.cube)
    pivot = args.pivot_corner
    if not CornerPosition.is_valid_string(pivot):
        error_and_exit(f'Invalid pivot [{pivot}]. Pivot must follow this format: (L|R)(D|U)(B|F)')
    pivot_str = f'{pivot} ({CornerPosition.from_string(pivot)})'
    if face_colors:
        pivot_str += f' {corner_to_colors(pivot, face_colors)}'
    print(f'Pivot: {pivot_str}')

    if not target_pattern.check_parity():
        error_and_exit(f'The target pattern [{target_pattern}] has wrong parity')
    if not target_pattern.is_solvable(pivot):
        error_and_exit(f'The target pattern [{target_pattern}] cannot be obtained with pivot {pivot} ({CornerPosition.from_string(pivot)})')

    allowed_rotations = rotations_from_pivot(args.pivot_corner)

    def found_predicate(cube: Cube):
        return target_pattern.match(cube)

    def process_solution(state: Cube, rotations: Algorithm):
        print(f'{state} {len(rotations)} [ {str(rotations)} ]', flush=True)

    explore_solutions = ExploreSolutions(allowed_rotations, found_predicate, process_solution)
    found = False
    depth = 1
    while (args.goto_max_depth or not found) and depth <= args.max:
        print(f'Recurse depth: {depth} {funny_hint(depth)}', flush=True)
        found = explore_solutions.recursive_dfs_exploration(depth)
        depth = depth + 1


if __name__ == "__main__":
    main()
