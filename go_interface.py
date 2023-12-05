"""
Import Statements
"""
import time

import gtp.gtp
from go_processing import *
from lcd import lcd_visuals
from gtp import gtp
from motor import Motors
from AppOpener import open
import os
import random
import string
import pexpect.popen_spawn as pex  # TODO CHANGE TO pexpect WHEN PULLED TO LINUX
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
    while not (val == "B" or val == "W"):
        visual.output()

        val = input("B or W")
        visual.set_input("Color?", "'B' or 'W': " + val)

    if val == "B":
        val = "black"
        visual.set_input("You are Black", "Good Luck!")
    else:
        val = "white"
        visual.set_input("You are White", "Good Luck!")
    visual.output()
    return str(val)


def get_vertex(visuals, board):
    all_char = "ABCDEFGHIJKMNOPQRSTUVWXYZ"
    valid_chars = all_char[: board.size]
    # input validation
    visuals.set_input("Enter your move", "Letter Number")
    valid_input_given = False
    user_input = None
    while not valid_input_given:
        visuals.output()
        user_input = input("enter your move").upper()
        if user_input == "pass" or user_input == "resign":
            valid_input_given = True
        elif (
            user_input[0] in valid_chars
            and user_input[1:].isdigit()
            and 1 <= int(user_input[1:]) <= board.size
        ):
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


def gLCL(vertex, board, stone_type, motor):
    remove_lst = []

    if vertex == gtp.PASS:  # Did they pass
        if board.fp:
            board.eg = True
        else:
            board.fp = True
    else:
        motor.move(from_gtp(vertex, board.size), stone_type)  # move to the space
        print("Putting Stone", vertex)
        remove_lst = board.update_game_arr(vertex, stone_type)
        board.fp = False
    if len(remove_lst) > 0:
        print("Removing: ", str(len(remove_lst)), "Nodes from board")
        motor.multi_move(remove_lst, stone_type)  # remove all the stones from the move


def parseScore(score, panel):
    splitted = score.split("+")
    color = splitted[0]
    score = splitted[1]
    if color == "b":
        print("Black won with a score of ", score)
    else:
        print("White won with a score of ", score)


def getModel(panel):
    level = -1
    panel.set_input("Select Difficulty", "1-12: ")
    while 1 <= level <= 12:
        panel.output()
        level = input("Select Difficulty")
        if not level.isdigit():
            panel.set_input("Use a number", "from 1-12")
        else:
            panel.set_input("Select Difficulty", "1-12:")
    panel.set_input("Difficulty:{}".format(level), "")
    print(level)
    panel.output()
    time.sleep(1000)
    return level


def gnugo_init():
    AI = pex.PopenSpawn("gnugo --mode gtp", encoding="utf-8")
    AI.sendline("boardsize 9")
    AI.sendline("clear_board")
    return AI


def katago_init():
    AI = pex.PopenSpawn("katago.exe gtp", encoding="utf-8")
    return AI


def find_file(panel, file_ext):
    if len(file_ext) <= 16:
        panel.set_input(file_ext, "")
    elif len(file_ext) <= 32:
        first = file_ext[:16]
        half = file_ext[16:]
        panel.set_input(first, half)
    else:
        raise Exception("TOOO LONG!!!!")


def main():
    panel = lcd_visuals()
    level = getModel(panel)
    AI = None
    if level < 12:
        AI = gnugo_init()
    else:
        AI = katago_init()
    f_name = generate_valid_file_path()
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
    motor = Motors(game_processor, AI_col, Player_Color)
    while game_processor.eg is False:
        if Player_Color == "black":
            print(game_processor)
            vertex = get_vertex(panel, game_processor)
            AI.sendline("play black {}".format(vertex))
            AI.expect("=")
            if not (vertex == gtp.RESIGN or vertex == gtp.PASS):
                gLCL(vertex, game_processor, gtp.BLACK, motor)
            else:
                break
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
            AI.sendline("play white {}".format(vertex))
            AI.expect("=")
            if not (vertex == "resign" or vertex == "pass"):
                gLCL(vertex, game_processor, gtp.WHITE, motor)
            else:
                break
            print(game_processor)

    print(game_processor)
    AI.sendline("final_score")
    AI.expect("[\w][+]\d+[.]\d")
    score = AI.after
    parseScore(score, panel)
    game_processor.create_sgf()
    print("Game Has ended")
    print("Please find your game at ", game_processor.file_out_name)
    find_file(panel, f_name)
    panel.output()
    print("We hope you have had an fun time with out unique way with playing Go!!")
    AI.sendline("quit")  # End AI Instance
    print("Credits; Sean Lai, Andy Li, Ray Eu, Safhira Hack")
    open("sabaki")


main()
