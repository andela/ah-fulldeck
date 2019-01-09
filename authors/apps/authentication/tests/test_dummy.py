import unittest


class Integration(unittest.TestCase):
    def test_dummy_for_travis_badge(self):
        result = (3+3)
        self.assertEqual(6, result)


if __name__ == '__main__':
    unittest.main()
