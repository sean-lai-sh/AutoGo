"""
Import Statements
"""
from go_processing import Sgf_Process, GTPFacade, from_gtp, text_to_gtp
from lcd import lcd_visuals
from gtp import gtp
from motor import motors
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


def get_setting():
    val = 0
    val = input("Input level of AI (1-12)")
    while not (isinstance(val, int) and 1 <= int(val) <= 12):
        print("ERROR: Invalid input please type a number from 1 - 12")
        val = input("Input level of AI (1-12)")
    if val == 12:
        return "LZBT"
    return str(val)


def init_ai():
    level_setting = get_setting()  # Query Input for other settings I.e Komi & what not
    AI_settings = ""
    if level_setting == "LZBT":
        AI_settings = values.gen_leelazero_preset()
        print("Playing against LeelaZero with Human Weights as White with 6.5 Komi")
    else:
        AI_settings = values.gen_gnugo_preset()  # Use our preset values to save time for comission testing
        AI_settings.append(level_setting)
        print("Playing against GNUGo Algorithm with 6.5 Komi")
    AI = GTPFacade("white",
                   AI_settings)  # Set it to white. Future versions need to implement player choosing starting sides
    AI.boardsize(9)  # Set boardsize to a 9x9 square. Change function if board used is a bigger one
    AI.komi(6.5)  # Default komi behavior
    AI.clear_board()  # Ensure previous
    return AI


def get_vertex():
    # input validation
    valid_input_given = False
    user_input = None
    while not valid_input_given:
        print(user_input)
        user_input = input("enter your move I.e A1").upper()
        if user_input == "PASS":
            valid_input_given = True
        elif user_input[0] in "ABCDEFGHI" and user_input[1:].isdigit() and 1 <= int(user_input[1:]) <= 9:
            valid_input_given = True
        else:
            print("Invalid move, do", "Letter Number")

    return text_to_gtp(user_input)


"""
Input:
game_input : a gtp coordinate
board: a board class object
motor: motors object

Function determines 
if game is ending here,
else 
1. move the stones to the spot
2. Update our Sgf_Process object game state 
3. Remove any stone(s) from our initial move
"""
def game_logic(game_input, board: Sgf_Process, motor: motors):
    global first_pass, end_game
    remove_lst = []

    if game_input == gtp.PASS:  # Did they pass
        if first_pass:
            end_game = True
        else:
            first_pass = True
    else:
        motor.move(game_input)  # move to the space
        print("Putting Stone", game_input)
        remove_lst = board.update_game_arr(gtp.BLACK, game_input)
        first_pass = False
    if len(remove_lst) > 0:
        print("Removing: ", str(len(remove_lst)), "Nodes from board")
        motor.multi_move(remove_lst)  # remove all the stones from the move


def start_player_vs_ai():
    # Query Input for mode
    global end_game, first_pass
    LCD = lcd_visuals()
    # Init GnuGo
    AI = init_ai()
    motorSys = motors()
    f_name = generate_valid_file_path()
    game_board = Sgf_Process(9, f_name, AI)
    end_game, first_pass = False, False
    while end_game is False:
        vertex = get_vertex()  # TO Implement
        game_logic(vertex, game_board, motorSys)  # Process input regarding game state, update Sgf
        AI.play(gtp.BLACK, vertex)  # Play move in AI engine
        # Vertex to Actual Motor

        # Sleep while waiting
        time.sleep(Sleep_Constant)  # Wait if need to remove
        AI.showboard()  # Display via Ascii for debugging
        vertex = AI.genmove(gtp.WHITE)  # Generate a move
        coordinate_out = ", ".join(from_gtp(vertex, 9))  # Get string of display coord to row col
        LCD.set_input("AI Plays at", coordinate_out)  # Print it out through LCD
        game_logic(vertex, game_board, motorSys)  # Process input for AI
        time.sleep(Sleep_Constant)  # Sleep if needed

    final_score = AI.final_score()  # Store the final score
    AI.close()
    game_board.create_sgf()  # Create a file
    AI.showboard()

    # Start Game
    # End game when needed
    return final_score
