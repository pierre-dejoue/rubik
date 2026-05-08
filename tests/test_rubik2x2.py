"""
Unit tests of the rubik2x2 module
"""
import unittest

from rubik2x2 import Algorithm, CWQuarterRot, cw_quarter_rotation_to_string, RepeatRot


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


class TestAlgorithm(unittest.TestCase):
    """Test the Algorithm class"""

    def test_apply(self):
        self.assertEqual(repr(Algorithm().apply()),                        "01234567:00000000")
        self.assertEqual(repr(Algorithm.from_string("F").apply()),         "01237456:00002121")
        self.assertEqual(repr(Algorithm.from_string("B D B L D").apply()), "07341265:21200202")

    def test_cyclic_order(self):
        self.assertEqual(Algorithm().cyclic_order(),                        1)
        self.assertEqual(Algorithm.from_string("R" ).cyclic_order(),        4)
        self.assertEqual(Algorithm.from_string("R2").cyclic_order(),        2)
        self.assertEqual(Algorithm.from_string("X" ).cyclic_order(),        4)
        self.assertEqual(Algorithm.from_string("D'").cyclic_order(),        4)
        self.assertEqual(Algorithm.from_string("B D B L D").cyclic_order(), 18)

    def test_repr(self):
        self.assertEqual(repr(Algorithm()),                           "")
        self.assertEqual(repr(Algorithm.from_string("F")),            "F")
        self.assertEqual(repr(Algorithm.from_string("B D2 B' L3 I")), "B D2 B3 L3")     # Note that B' became B3

    def test_to_str(self):
        self.assertEqual(str(Algorithm()),                            "")
        self.assertEqual(str(Algorithm.from_string("F")),             "F")
        self.assertEqual(str(Algorithm.from_string("B D2 B' L3 I")),  "B D2 B' L'")


if __name__ == '__main__':
    unittest.main()
