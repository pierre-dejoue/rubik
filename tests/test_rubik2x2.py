import unittest

from rubik2x2 import Rotation


class TestRotation(unittest.TestCase):
    def test_base_rotations_are_valid(self):
        self.assertTrue(Rotation.L.is_valid())
        self.assertTrue(Rotation.R.is_valid())
        self.assertTrue(Rotation.D.is_valid())
        self.assertTrue(Rotation.U.is_valid())
        self.assertTrue(Rotation.B.is_valid())
        self.assertTrue(Rotation.F.is_valid())
        self.assertTrue(Rotation.X.is_valid())
        self.assertTrue(Rotation.Y.is_valid())
        self.assertTrue(Rotation.Z.is_valid())

    def test_rot_axis(self):
        self.assertEqual(Rotation.L.axis, Rotation.R.axis)
        self.assertEqual(Rotation.D.axis, Rotation.U.axis)
        self.assertEqual(Rotation.B.axis, Rotation.F.axis)
        self.assertNotEqual(Rotation.L.axis, Rotation.D.axis)
        self.assertNotEqual(Rotation.L.axis, Rotation.B.axis)
        self.assertNotEqual(Rotation.D.axis, Rotation.B.axis)

    def test_rot_to_string(self):
        self.assertEqual(Rotation.L.to_string(0), "I")
        self.assertEqual(Rotation.L.to_string(1), "L")
        self.assertEqual(Rotation.L.to_string(2), "L2")
        self.assertEqual(Rotation.L.to_string(3), "L'")


if __name__ == '__main__':
    unittest.main()
