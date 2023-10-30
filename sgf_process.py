import numpy as np
from sgfmill import sgf
from sgfmill import sgf_board_interface
from gtp import gtp
from gtp_initialize import GTPFacade
from enum import IntEnum


class Stone_type(IntEnum):
    black = 1
    white = -1
    empty = 0


class Sgf_process:
    def __init__(self, size, file_name, AI_reference):
        # Init Output file that Sabaki can later open
        self.file_out_name = file_name
        self.size = size
        # Init Game
        # self.game = sgf.Sgf_game(size=self.size)
        self.AI = AI_reference
        # self.game_arr = np.zeros((self.size, self.size))
        # self.board = np.zeros((self.size,self.size))
        self.board = file_name

    def update_game_arr(self, gtp_vertex, TYPE: Stone_type):
        # ASSUMES THAT TYPE IS BLACK OR WHITE VALUED AS 1 or -1 RESPECTIVELY
        coordinate = get_row_col(gtp_vertex)
        self.board[coordinate[0]][coordinate[1]] = TYPE

    def remove_stone_path(self, array, sgf):
        """
        :param array:
        :param sgf:
        :return: linked list or ordered list of paths to remove stones from current location of removing stone tool
        """

    def remove(self, color: Stone_type, s_coord, to_check, lst_out):
        check_sum = len(to_check)
        final_lst = []
        for coord in to_check:
            x, y = coord[0], coord[1]
            if not ((0 < x < len(self.board)) and (-1 < y < len(self.board))):
                check_sum -= 1
            elif self.board[x][y] == -color:
                check_sum -= 1
            elif self.board[x][y] == color:
                new_check = np.array([[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]])
                for k in range(len(new_check)):
                    if new_check[k][0] == s_coord[0] and new_check[k][1] == s_coord[1]:
                        np.delete(new_check, k, 0)
                print("NewCheck:",new_check)
                # check_sum -= self.remove(color, [x, y], new_check, final_lst)
            # print(check_sum, coord)
        if check_sum == 0:
            final_lst.append(s_coord)
            lst_out[:] = final_lst[:]
            return -1
        else:
            return 0

    def move_stone_path(self, array, sgf):
        pass

    def identify(self):
        pass
