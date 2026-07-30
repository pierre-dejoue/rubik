"""
Unit tests of the rubik2x2 module
"""
import unittest

from rubik2x2 import (
    Algorithm,
    Cube,
    CubeSolver,
    CWQuarterRot,
    RepeatRot,
    cw_quarter_rotation_to_string,
    rotations_from_pivot,
)


class TestCWQuarterRot(unittest.TestCase):
    """Test the CWQuarterRot namespace"""

    def test_clockwise_quarter_rotations_are_valid(self):
        self.assertTrue(CWQuarterRot.L.is_valid())
        self.assertTrue(CWQuarterRot.R.is_valid())
        self.assertTrue(CWQuarterRot.D.is_valid())
        self.assertTrue(CWQuarterRot.U.is_valid())
        self.assertTrue(CWQuarterRot.B.is_valid())
        self.assertTrue(CWQuarterRot.F.is_valid())
        self.assertTrue(CWQuarterRot.X.is_valid())
        self.assertTrue(CWQuarterRot.Y.is_valid())
        self.assertTrue(CWQuarterRot.Z.is_valid())

    def test_rot_axis(self):
        self.assertEqual(CWQuarterRot.L.axis, CWQuarterRot.R.axis)
        self.assertEqual(CWQuarterRot.D.axis, CWQuarterRot.U.axis)
        self.assertEqual(CWQuarterRot.B.axis, CWQuarterRot.F.axis)
        self.assertNotEqual(CWQuarterRot.L.axis, CWQuarterRot.D.axis)
        self.assertNotEqual(CWQuarterRot.L.axis, CWQuarterRot.B.axis)
        self.assertNotEqual(CWQuarterRot.D.axis, CWQuarterRot.B.axis)

    def test_cw_quarter_rotation_to_string(self):
        self.assertEqual(cw_quarter_rotation_to_string(CWQuarterRot.L, 0), "I")
        self.assertEqual(cw_quarter_rotation_to_string(CWQuarterRot.L, 1), "L")
        self.assertEqual(cw_quarter_rotation_to_string(CWQuarterRot.L, 2), "L2")
        self.assertEqual(cw_quarter_rotation_to_string(CWQuarterRot.L, 3), "L'")
        self.assertEqual(cw_quarter_rotation_to_string(CWQuarterRot.L, 4), "I")
        self.assertEqual(cw_quarter_rotation_to_string(CWQuarterRot.L, 5), "L")


class TestRepeatRot(unittest.TestCase):
    """Test the RepeatRot class"""

    def test_repr(self):
        self.assertEqual(repr(RepeatRot(CWQuarterRot.U, 0)), "I")
        self.assertEqual(repr(RepeatRot(CWQuarterRot.U, 1)), "U")
        self.assertEqual(repr(RepeatRot(CWQuarterRot.U, 2)), "U2")
        self.assertEqual(repr(RepeatRot(CWQuarterRot.U, 3)), "U3")  # Not U'
        self.assertEqual(repr(RepeatRot(CWQuarterRot.U, 4)), "U4")
        self.assertEqual(repr(RepeatRot(CWQuarterRot.U, 5)), "U5")

    def test_identity(self):
        id_rot = RepeatRot.identity()
        self.assertEqual(repr(id_rot), "I")


class TestCube(unittest.TestCase):
    """Test the Cube class"""

    # An example of a cube configuration, without a pivot, with the theoretical maximum cyclic_order 45 (=3*5*3)
    CUBE_CYCLIC_ORDER_45 = '45126703:01200210'

    # An example of a cube configuration, with a pivot, and the max theoretical cyclic_order 36 (=3*4*3)
    CUBE_CYCLIC_ORDER_36 = '12035674:10002000'

    # An example of a cube configuration, with a pivot, with cyclic_order 30 (=3*5*2)
    CUBE_CYCLIC_ORDER_30 = '05126743:01200210'

    def test_init(self):
        self.assertEqual(repr(Cube.solved()),                                            "01234567:00000000")
        self.assertEqual(repr(Cube([0, 1, 2, 3, 7, 4, 5, 6], [0, 0, 0, 0, 2, 1, 2, 1])), "01237456:00002121")

    def test_permutation_cycles(self):
        def static_position_to_cycles(cube_str: str) -> list[set[int]]:
            return list(map(set, Cube.from_string(cube_str).permutation_cycles()))
        self.assertEqual(static_position_to_cycles(self.CUBE_CYCLIC_ORDER_45), [{1, 2, 3, 5, 7}, {0, 4, 6}])
        self.assertEqual(static_position_to_cycles(self.CUBE_CYCLIC_ORDER_36), [{4, 5, 6, 7}, {0, 1, 2}, {3}])
        self.assertEqual(static_position_to_cycles(self.CUBE_CYCLIC_ORDER_30), [{1, 2, 3, 5, 7}, {4, 6}, {0}])

    def test_cyclic_order(self):
        self.assertEqual(Cube.from_string(self.CUBE_CYCLIC_ORDER_45).cyclic_order(), 45)
        self.assertEqual(Cube.from_string(self.CUBE_CYCLIC_ORDER_36).cyclic_order(), 36)
        self.assertEqual(Cube.from_string(self.CUBE_CYCLIC_ORDER_30).cyclic_order(), 30)


class TestAlgorithm(unittest.TestCase):
    """Test the Algorithm class"""

    def test_apply(self):
        self.assertEqual(repr(Algorithm().apply()),                        "01234567:00000000")
        self.assertEqual(repr(Algorithm.from_string("I").apply()),         "01234567:00000000")
        self.assertEqual(repr(Algorithm.from_string("F").apply()),         "01237456:00002121")
        self.assertEqual(repr(Algorithm.from_string("R F").apply()),       "04137526:02202111")
        self.assertEqual(repr(Algorithm.from_string("R B").apply()),       "15204637:11120220")
        self.assertEqual(repr(Algorithm.from_string("R U").apply()),       "05124763:01200210")
        self.assertEqual(repr(Algorithm.from_string("B D B L D").apply()), "07341265:21200202")
        self.assertEqual(repr(Algorithm.from_string("B D B R D").apply()), "13456027:00022110")

    def test_cyclic_order(self):
        self.assertEqual(Algorithm().cyclic_order(),                        1)
        self.assertEqual(Algorithm.from_string("I" ).cyclic_order(),        1)
        self.assertEqual(Algorithm.from_string("R" ).cyclic_order(),        4)
        self.assertEqual(Algorithm.from_string("R2").cyclic_order(),        2)
        self.assertEqual(Algorithm.from_string("X" ).cyclic_order(),        4)
        self.assertEqual(Algorithm.from_string("D'").cyclic_order(),        4)
        self.assertEqual(Algorithm.from_string("R F").cyclic_order(),       15)
        self.assertEqual(Algorithm.from_string("R B").cyclic_order(),       15)
        self.assertEqual(Algorithm.from_string("R U").cyclic_order(),       15)
        self.assertEqual(Algorithm.from_string("B D B L D").cyclic_order(), 18)
        self.assertEqual(Algorithm.from_string("B D B R D").cyclic_order(), 12)

    def test_permutation_cycles(self):
        def algo_to_cycle_lengths(algo: str) -> list[int]:
            cube = Algorithm.from_string(algo).apply()
            return list(map(len, cube.permutation_cycles()))
        self.assertEqual(algo_to_cycle_lengths("R"),         [4, 1, 1, 1, 1])
        self.assertEqual(algo_to_cycle_lengths("R2"),        [2, 2, 1, 1, 1, 1])
        self.assertEqual(algo_to_cycle_lengths("X"),         [4, 4])
        self.assertEqual(algo_to_cycle_lengths("R U"),       [5, 1, 1, 1])
        self.assertEqual(algo_to_cycle_lengths("B D B L D"), [6, 1, 1])
        self.assertEqual(algo_to_cycle_lengths("B D B R D"), [4, 3, 1])

    def test_cube_fixed_corners(self):
        test_cases = [
            ("R U",         [6],    [0, 4]),
            ("D'",          [],     [2, 3, 6, 7]),
            ("B D B L D",   [0],    [6] )
        ]
        for algo_str, expected_fixed_pos_not_ori, expected_fixed_pos_and_ori in test_cases:
            with self.subTest(algo=algo_str):
                fixed_pos_not_ori, fixed_pos_and_ori = Algorithm.from_string(algo_str).apply().fixed_corners()
                self.assertEqual(fixed_pos_not_ori, expected_fixed_pos_not_ori)
                self.assertEqual(fixed_pos_and_ori, expected_fixed_pos_and_ori)

    def test_repr(self):
        self.assertEqual(repr(Algorithm()),                           "")
        self.assertEqual(repr(Algorithm.from_string("F")),            "F")
        self.assertEqual(repr(Algorithm.from_string("R B")),          "R B")
        self.assertEqual(repr(Algorithm.from_string("B D2 B' L3 I")), "B D2 B3 L3")     # Note that B' became B3

    def test_to_str(self):
        self.assertEqual(str(Algorithm()),                            "")
        self.assertEqual(str(Algorithm.from_string("F")),             "F")
        self.assertEqual(str(Algorithm.from_string("R B")),           "R B")
        self.assertEqual(str(Algorithm.from_string("B D2 B' L3 I")),  "B D2 B' L'")


class TestModuleFunctions(unittest.TestCase):
    """Test functions at the module level"""

    def test_rotations_from_pivot(self):
        self.assertEqual({ r.name for r in rotations_from_pivot('LUF') }, { 'R', 'D', 'B' })
        self.assertEqual({ r.name for r in rotations_from_pivot('RDB') }, { 'L', 'U', 'F' })


class TestExploreSolutions(unittest.TestCase):
    """Test classes ExploreSolutions and CubeSolver"""

    def test_cube_solver(self):
        test_cases = [
        #    scramble_algo, pivot,  search_depth,   expected_found, expected_algos, expected_algo_len
            ("R U",         'LDB',  1,              False,          0,              0),
            ("R U",         'LDB',  2,              True,           1,              2),
            ("R U",         'LDB',  3,              True,           1,              2),
        ]
        for scramble_algo, pivot, search_depth, expected_found, expected_algos, expected_algo_len in test_cases:
            with self.subTest(depth = search_depth):
                cube_to_solve = Algorithm.from_string(scramble_algo).apply()
                found_algos = []
                solver = CubeSolver(rotations_from_pivot(pivot), lambda _, a: found_algos.append(a), cube_to_solve)
                self.assertEqual(solver.dfs_exploration(search_depth), expected_found)
                self.assertEqual(len(found_algos), expected_algos)
                for algo in found_algos:
                    self.assertEqual(len(algo), expected_algo_len)


if __name__ == '__main__':
    unittest.main()
