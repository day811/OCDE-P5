# test module
import unittest

import migration_script as ms




class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = ms.sum(data)
        self.assertEqual(result, 6)

if __name__ == "__main_":
    unittest.main()
