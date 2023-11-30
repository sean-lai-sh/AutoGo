# import numpy as np
# from sgfmill import sgf
# from go_processing import Sgf_Process, Stone_type
#
#
# # # Reading game from bytes: TO CHANGE TO GAME FILE ONCE CODES READY
# # game_processing = Sgf_process()
# # ### game_arr => interface with the motors
# # game = game_processing.game
# # game_arr = [[None for i in range(9)] for k in range(9)]
# # game_board, plays = sgf_moves.get_setup_and_moves(game)
# # print(ascii_boards.render_board(game_board))
#
# def vertex_to_idx(vertex):
#     Str_val = vertex[0].lower()
#     int_val = "".join(vertex[1:])
#     row = chr(97 + int(int_val))
#     col = Str_val
#     return col + row
#
#
# print(vertex_to_idx("A19"))
#
# ### Writing a game file: upon input
# # BASE CASE
# # test_arr = np.array([[1, -1], [-1, 0]])
# # test_sgf = Sgf_process(2, test_arr, "")
# # re_lst = []
# # print(test_arr)
# # x = 0
# # y = 0
# # tc = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
# # re_lst = test_sgf.remove(Stone_type.black, np.array([x, y]), tc)[1]
# # print("re", re_lst)
# board = np.array([
#     [1, 0, 1, 1, -1, 1, 0],
#     [1, -1, 1, 1, -1, 1, 1],
#     [1, 1, -1, 1, -1, 1, 1],
#     [-1, -1, 0, -1, 1, -1, -1],
#     [0, 0, 0, 1, 0, 0, -1],
#     [0, 0, 0, 0, 0, -1, 1],
#     [0, 0, 0, 0, 0, 0, 1],
# ])
# ## 0,0 1,0 2,1 0,2 1,2 0,3 1,3 2,3
# # test_sgf2 = Sgf_process(7, board, "")
# # re_lst2 = []
# # final_lst = test_sgf2.remove(Stone_type.black, [0,0], std_check([0,0]))
# # print("re_lst2:", final_lst)
# # print()
# #
# board2 = np.array([
#     [1, -1, 1, 1],
#     [1, -1, -1, -1],
#     [1, 1, -1, 0],
#     [-1, -1, 0, 0],
# ])
# test3 = Sgf_Process(7, file_name="", AI_reference=board)
# print(test3.update_game_arr("B7", Stone_type.white))
# print(test3)
import pexpect.popen_spawn as ps
import sys

game = ps.PopenSpawn("gnugo --mode gtp", encoding='utf-8')
game.sendline("1 boardsize 9")
game.expect('=1') # Tells us when command is stopped/ processed
print(game.after) # Returns the data the expect was given or matched
game.sendline("showboard") # Write the code as if it was correct
game.expect("=")
print(game.after)
