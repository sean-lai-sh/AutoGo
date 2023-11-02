import numpy as np
from sgfmill import sgf, sgf_board_interface
from gtp import gtp
from gtp_initialize import GTPFacade
from enum import IntEnum


class Stone_type(IntEnum):
    black = 1
    white = -1
    empty = 0


def gtp_to_sgf(vertex, board_size):
    init_conv = from_gtp(vertex, board_size)
    to_conv = to_sgf(init_conv)
    return to_conv


def text_to_gtp(coord_str):
    letter_val = coord_str[0].upper()
    if letter_val == "I":
        letter_val = "J"
    return letter_val + coord_str[1:]


def from_gtp(gtpc, bs):
    """Converts from a GTP coordinate to a Minigo coordinate."""
    gtpc = gtpc.upper()
    if gtpc == 'PASS':
        return None
    col = _GTP_COLUMNS.index(gtpc[0])
    row_from_bottom = int(gtpc[1:])
    return bs - row_from_bottom, col


def to_sgf(coord):
    """Converts from a Minigo coordinate to an SGF coordinate."""
    if coord is None:
        return ''
    return _SGF_COLUMNS[coord[1]] + _SGF_COLUMNS[coord[0]]


_SGF_COLUMNS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_GTP_COLUMNS = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'


def std_check(coord):
    x, y = coord[0], coord[1]
    tc = np.array([[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]])
    return tc


def to_color(TYPE):
    if TYPE == Stone_type.black:
        return 'b'
    else:
        return 'w'


class Sgf_process:
    def __init__(self, size, file_name, AI_reference):
        # Init Output file that Sabaki can later open
        self.file_out_name = file_name
        self.size = size
        # Init Game
        self.game = sgf.Sgf_game(size=self.size)
        # self.game = AI_reference
        # self.game_arr = np.zeros((self.size, self.size))
        self.board = AI_reference
        # self.board = AI_reference
        self.checked_lst = []

    def update_game_arr(self, gtp_vertex, TYPE: Stone_type):
        # ASSUMES THAT TYPE IS BLACK OR WHITE VALUED AS 1 or -1 RESPECTIVELY
        coordinate = from_gtp(gtp_vertex, self.size)
        print(coordinate)
        # gtp -> minigo, i.e row col format
        # print(coordinate[0], coordinate[1])
        self.board[coordinate[0]][coordinate[1]] = TYPE
        to_check = std_check(coordinate)
        final_lst = []
        print("Checking indices:", to_check)
        for t_coord in to_check:
            if self.isValid(t_coord) and self.board[t_coord[0]][t_coord[1]] == -TYPE:
                data = self.std_remove(-TYPE, t_coord)[1]
                 # print("Data:", data)
                if len(final_lst) > 0:
                    final_lst.extend(data)
                else:
                    final_lst = data
        sgf_coord = to_sgf(coordinate)
        # print(sgf_coord)
        sgf_color = to_color(TYPE)
        # print(sgf_color)
        self.add_to_sgf([sgf_color, coordinate, None])
        for k in final_lst:
            x, y = k[0], k[1]
            self.board[x][y] = Stone_type.empty
        return final_lst

    def isValid(self, coord):
        return (-1 < coord[0] < self.size) and (-1 < coord[1] < self.size)

    def remove_stone_path(self, array, sgf):
        """
        :param array:
        :param sgf:
        :return: linked list or ordered list of paths to remove stones from current location of removing stone tool
        """

    def std_remove(self, color: Stone_type, coords):
        return self.remove(color, coords, std_check(coords))

    def remove(self, color: Stone_type, s_coord, to_check):
        self.checked_lst.append(s_coord)
        check_sum = len(to_check)
        final_lst = []
        # print("Current Coord to check: ", s_coord)
        # print("Current Coords to Check", to_check)
        for coord in to_check:
            x, y = coord[0], coord[1]
            if not self.isValid(coord):
                check_sum -= 1
            elif self.board[x][y] == -color:
                check_sum -= 1
            elif self.board[x][y] == color:
                new_check = std_check(coord)
                next_check = self.prev_dup(new_check, self.checked_lst)
                print(self.checked_lst)
                next_s = self.remove(color, [x, y], next_check)
                # print(next_s)
                check_sum += next_s[0]
                final_lst = final_lst + next_s[1]
        # print(check_sum)
        if check_sum <= 0:
            # print("Stone coords", s_coord)
            final_lst.append(s_coord)
            return -1, final_lst
        else:
            return 0, final_lst

    def move_stone_path(self, array, file):
        pass

    def prev_dup(self, to_check, checked):
        k = 0
        l_n_c = len(to_check)
        to_re = to_check.copy()
        while k < l_n_c:
            was_found = False
            for s_coord in checked:
                if np.array_equal(to_re[k], s_coord):
                    to_re = np.delete(to_re, k, 0)
                    l_n_c -= 1
                    was_found = True
                    break
            if not was_found:
                k += 1
        return to_re

    def add_to_sgf(self, move_data):
        node = self.game.extend_main_sequence()
        node.set_move(move_data[0], move_data[1])
        if move_data[2] is not None:
            node.set("C", move_data.comment)
        print(move_data)

    def identify(self):
        pass

    def create_sgf(self):
        try:
            with open(self.file_out_name, "wb") as f:
                f.write(self.game.serialise())
            return True
        except FileNotFoundError:
            return False
