import numpy as np
from sgfmill import sgf
from sgfmill import sgf_moves
from sgfmill import ascii_boards
from sgf_process import Sgf_process, Stone_type, std_check

from sgfmill import ascii_boards


# # Reading game from bytes: TO CHANGE TO GAME FILE ONCE CODES READY
# game_processing = Sgf_process()
# ### game_arr => interface with the motors
# game = game_processing.game
# game_arr = [[None for i in range(9)] for k in range(9)]
# game_board, plays = sgf_moves.get_setup_and_moves(game)
# print(ascii_boards.render_board(game_board))

def vertex_to_idx(vertex):
    Str_val = vertex[0].lower()
    int_val = "".join(vertex[1:])
    row = chr(97 + int(int_val))
    col = Str_val
    return col + row


print(vertex_to_idx("A19"))

### Writing a game file: upon input
# BASE CASE
test_arr = np.array([[1, -1], [-1, 0]])
test_sgf = Sgf_process(2, test_arr, "")
re_lst = []
print(test_arr)
x = 0
y = 0
tc = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
re_lst = test_sgf.remove(Stone_type.black, np.array([x, y]), tc)[1]
print("re", re_lst)
board = np.array([
    [1, -1, 0, 0, -1, 1, 0],
    [1, -1, 0, 0, -1, 1, 1],
    [1, 1, -1, 1, -1, 1, 1],
    [-1, -1, 1, -1, 1, -1, -1],
    [0, 0, 0, 1, 0, 0, -1],
    [0, 0, 0, 0, 0, -1, 1],
    [0, 0, 0, 0, 0, 0, 1],
])
test_sgf2 = Sgf_process(7, board, "")
re_lst2 = []
final_lst = test_sgf2.remove(Stone_type.black, [0,0], std_check([0,0]))
print("re_lst2:", final_lst)
