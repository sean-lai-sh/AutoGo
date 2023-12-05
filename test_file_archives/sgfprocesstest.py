import unittest
import numpy as np
from go_processing import *
from gtp import gtp


class MyTestCase(unittest.TestCase):
    def test_base(self):
        test_arr = np.array([[1, 0], [-1, 0]])
        test_sgf = Sgf_Process(2, "", "", test_arr)
        re_lst = []
        x = 0
        y = 1
        tc = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        re_lst = test_sgf.remove(gtp.BLACK, np.array([x, y]), tc)[1]
        print(re_lst)
        self.assertEqual([[0, 0]], re_lst)

    def test_multi_remove(self):
        board = np.array(
            [
                [1, 0, 1, 1, -1, 1, 0],
                [1, -1, 1, 1, -1, 1, 1],
                [1, 1, -1, 1, -1, 1, 1],
                [-1, -1, 0, -1, 1, -1, -1],
                [0, 0, 0, 1, 0, 0, -1],
                [0, 0, 0, 0, 0, -1, 1],
                [0, 0, 0, 0, 0, 0, 1],
            ]
        )
        ## 0,0 1,0 2,1 0,2 1,2 0,3 1,3 2,3
        correct_lst = [
            [2, 3],
            [0, 3],
            [1, 3],
            [1, 2],
            [0, 3],
            np.array([0, 2]),
            [2, 1],
            [2, 0],
            [1, 0],
            np.array([0, 0]),
        ]
        test_sgf2 = Sgf_Process(7, "", "", board)
        re_lst2 = []
        final_lst = test_sgf2.update_game_arr("B7", gtp.WHITE)
        self.assertEqual(correct_lst, final_lst)
        # print()


if __name__ == "__main__":
    unittest.main()
