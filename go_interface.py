"""
Import Statements
"""
import gtp.gtp
from go_processing import *
from lcd import lcd_visuals
from gtp import gtp
from motor import motors
import os
import random
import string
import pexpect.popen_spawn as pex #TODO CHANGE TO pexpect WHEN PULLED TO LINUX
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
    visual.set_input("Input level", "of AI: 1-11")
    while not (isinstance(val, int) and 1 <= int(val) <= 12):
        val = input("Input level of AI")
    if val == 12:
        return "LZBT"
    return str(val)

def get_color(visual: lcd_visuals):
    val = ""
    visual.set_input("Color?", "'B' or 'W': " + val)
    while not (val == 'B' or val =='W'):
        visual.output()

        val = input("B or W")
        visual.set_input("Color?", "'B' or 'W': " + val)

    if val == 'B':
        val = "black"
        visual.set_input("You are Black", "Good Luck!")
    else:
        val = "white"
        visual.set_input("You are White", "Good Luck!")
    visual.output()
    return str(val)

def get_vertex(visuals, board):
    all_char = "ABCDEFGHIJKMNOPQRSTUVWXYZ"
    valid_chars = all_char[:board.size]
    # input validation
    visuals.set_input("Enter your move", "Letter Number")
    valid_input_given = False
    user_input = None
    while not valid_input_given:
        visuals.output()
        user_input = input("enter your move").upper()
        if user_input == "PASS":
            valid_input_given = True

        elif user_input[0] in valid_chars and user_input[1:].isdigit() and 1 <= int(user_input[1:]) <= board.size:
            valid_input_given = True

        else:
            visuals.set_input("Invalid. Type letter", "number. ex: A5")

    return text_to_gtp(user_input)


print_player_text = "Please make your decision: \n -Move i.e A3 \n -Pass: 'PASS' \n -resign: 'resign' \n Your Input:"

"""
Input:
game_input : a gtp coordinate
board: a board class object
stone_type: a gtp Const assumed to be denoting black or white
motor: motors object

Function determines 
if game is ending here,
else 
1. move the stones to the spot
2. Update our Sgf_Process object game state 
3. Remove any stone(s) from our initial move
"""
def gLCL(move, board, stone_type, motor):

    remove_lst = []

    if move == gtp.PASS:  # Did they pass
        if board.fp:
            board.eg = True
        else:
            board.fp = True
    else:
        motor.move(move)  # move to the space
        print("Putting Stone", move)
        remove_lst = board.update_game_arr(move, stone_type)
        board.fp = False
    if len(remove_lst) > 0:
        print("Removing: ", str(len(remove_lst)), "Nodes from board")
        motor.multi_move(remove_lst)  # remove all the stones from the move


def parseScore(score):
    splitted = score.split("+")
    color = splitted[0]
    score = splitted[1]
    if color == "b":
        print("Black won with a score of ", score)
    else:
        print("White won with a score of ", score)


def main():
    # model = input("Choose, gnugo or leelazero")
    AI = pex.PopenSpawn("gnugo --mode gtp", encoding="utf-8")
    AI.sendline("boardsize 9")
    AI.sendline("clear_board")
    motor = motors
    panel = lcd_visuals()
    f_name = ""
    game_processor = Sgf_Process(9, f_name, AI)
    Player_Color = get_color(panel)
    AI_col = None
    command = ""
    if Player_Color == "black":
        AI_col = gtp.WHITE
        command = "genmove white"
    else:
        AI_col = gtp.BLACK
        command = "genmove black"

    while game_processor.eg is False:
        if Player_Color == "black":
            print(game_processor)
            vertex = get_vertex(panel, game_processor)
            gLCL(vertex, game_processor, gtp.BLACK, motor)
            print(game_processor)

        AI.sendline(command)  # Generate Move
        AI.expect("[\w]{6}|[A-Z]\d{1,2}")  # Get move
        AI_move = AI.after
        if AI_move == gtp.RESIGN:
            print("AI has resigned you have won")
            panel.set_input("AI resigned", "you have won")
            break
        gLCL(AI_move, game_processor, AI_col, motor)

        if Player_Color == "white":
            print(game_processor)
            vertex = get_vertex(panel, game_processor)
            gLCL(vertex, game_processor, gtp.WHITE, motor)
            print(game_processor)

    print(game_processor)
    AI.sendline("final_score")
    AI.expect("[\w][+]\d+[.]\d")
    score = AI.after
    parseScore(score)
    game_processor.create_sgf()
    print("Game Has ended")
    print("Please find your game at ", game_processor.file_out_name)
    print("We hope you have had an fun time with out unique way with playing Go!!")
    AI.sendline("quit")  # End AI Instance
    print("Credits; Sean Lai, Andy Li, Ray Eu, Safhira Hack")


main()
