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
from go_processing import *
def vertex_to_idx(vertex):
    Str_val = vertex[0].lower()
    int_val = "".join(vertex[1:])
    row = chr(97 + int(int_val))
    col = Str_val
    return col + row


print(from_gtp("A19", 19))
#
### Writing a game file: upon input
import pexpect.popen_spawn as pex
import sys
from go_processing import *

game = pex.PopenSpawn("gnugo --mode gtp", encoding='utf-8')
game.sendline("boardsize 9")
game.sendline("clear_board")
game.expect('=') # Tells us when command is stopped/ processed
color = input("Pick black or white")
if color == "black":
    AI_color = "white"
else:
    AI_color = "black"
while True:
    game.sendline("genmove " + color) # Write the code as if it was correct
    game.expect("[A-Z]\d+")
    print(game.after)
    Coord = input("Input")
    game.sendline("play white " + Coord)
    game.expect("=")
    game.sendline("showboard")
    game.expect("[.{3,9}\n]+")
    print(game.after)


print(game.after)


