import os

from gtp_initialize import GTPFacade
from gtp import gtp
import time
import random
import string
from sgf_process import Sgf_process

Sleep_Constant = 10

PATH = "/"


def generate_valid_file_path():
    f_name = "test"
    ext_name = ".sgf"
    while not os.path.isfile(PATH + f_name + ext_name):
        f_name += random.choice(string.ascii_letters)
    return PATH + f_name + ext_name


def start_player_vs_ai():
    # Query Input for mode
    AI_settings = ["gnugo", "--mode", "gtp", "--level", "10"]
    AI = GTPFacade("white", AI_settings)
    AI.boardsize(9)
    AI.komi(6.5)
    AI.clear_board()
    first_pass = False
    f_name = generate_valid_file_path()
    game_board = Sgf_process(9, f_name, AI)
    while True:
        vertex = get_vertex()  # TO Implement
        if vertex == gtp.PASS:
            if first_pass:
                break
            else:
                first_pass = True
        else:
            game_board.update_game_arr(gtp.BLACK, vertex)
            first_pass = False
        AI.play(gtp.BLACK, vertex)
        # Vertex to Actual Motor

        #Sleep while waiting
        time.sleep(Sleep_Constant)
        AI.showboard()
        vertex = AI.genmove(gtp.WHITE)
        if vertex == gtp.PASS:
            if first_pass:
                break
            else:
                first_pass = True
        else:
            game_board.update_game_arr(gtp.WHITE, vertex)
            first_pass = False

        time.sleep(Sleep_Constant)

    final_score = AI.final_score()
    AI.close()
    game_board.create_sgf()
    # Query Input for other settings I.e Komi & what not
    # Init GnuGo
    # Start Game
    # End game when needed
    return final_score
