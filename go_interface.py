"""
Import Statements
"""
from go_processing import Sgf_process, GTPFacade, from_gtp
from lcd import lcd_visuals
from gtp import gtp
import os
import random
import string
import time
import values

Sleep_Constant = values.SLEEP_CONST

PATH = "/"

end_game = False  # Global Var for coroutine
first_pass = False


def generate_valid_file_path():
    f_name = "test"
    ext_name = ".sgf"
    while not os.path.isfile(PATH + f_name + ext_name):
        f_name += random.choice(string.ascii_letters)
    return PATH + f_name + ext_name


def get_setting(visual: lcd_visuals):
    val = 0
    while not (isinstance(val, int) and 1 <= int(val) <= 10):
        val = input("Input level of code")
    return str(val)


def init_ai(LCD):
    level_setting = get_setting(LCD)
    AI_settings = values.gen_gnugo_preset()
    AI_settings.append(level_setting)
    AI = GTPFacade("white", AI_settings)
    AI.boardsize(9)
    AI.komi(6.5)
    AI.clear_board()
    return AI


def get_vertex(visuals):
    # input validation
    visuals.set_input("Enter your move", "Letter Number")
    valid_input_given = False
    while not valid_input_given:
        visuals.output()
        user_input = input("enter your move").upper()
        if user_input[0] in "ABCDEFGHI" and user_input[1:].isdigit() and 1 <= user_input[1:] <= 9:
            valid_input_given = True
            continue
        visuals.set_input("Invalid move, do", "Letter Number")
    return user_input


def game_logic(game_input, board):
    global first_pass, end_game
    remove_lst = []
    if game_input == gtp.PASS:
        if first_pass:
            end_game = True
        else:
            first_pass = True
    else:
        remove_lst = board.update_game_arr(gtp.BLACK, game_input)
        first_pass = False
    if len(remove_lst) > 1:
        print("Removing: ", str(len(remove_lst)), "Nodes from board")


def start_player_vs_ai():
    # Query Input for mode
    global end_game, first_pass
    LCD = lcd_visuals()
    AI = init_ai(LCD)
    f_name = generate_valid_file_path()
    game_board = Sgf_process(9, f_name, AI)
    end_game, first_pass = False, False
    while end_game is False:
        vertex = get_vertex(LCD)  # TO Implement
        game_logic(vertex, game_board)  # Process input regarding game state, update Sgf
        AI.play(gtp.BLACK, vertex)  # Play move in AI engine
        # Vertex to Actual Motor

        # Sleep while waiting
        time.sleep(Sleep_Constant)  # Wait if need to remove
        AI.showboard()  # Display via Ascii for debugging
        vertex = AI.genmove(gtp.WHITE)  # Generate a move
        coordinate_out = ", ".join(from_gtp(vertex, 9))  # Get string of display coord to row col
        LCD.set_input("AI Plays at", coordinate_out)  # Print it out through LCD
        game_logic(vertex, game_board)  # Process input for AI
        time.sleep(Sleep_Constant)  # Sleep if needed

    final_score = AI.final_score()  # Store the final score
    AI.close()
    game_board.create_sgf()  # Create a file
    AI.showboard()
    # Query Input for other settings I.e Komi & what not
    # Init GnuGo
    # Start Game
    # End game when needed
    return final_score
