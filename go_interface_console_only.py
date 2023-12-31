from sgfprocess import *
import pexpect.popen_spawn as pex

print_player_text = "Please make your decision: \n -Move i.e A3 \n -Pass: 'PASS' \n -resign: 'resign' \n Your Input:"


def gLCL(move, board, stone_type):
    remove_lst = []

    if move == gtp.PASS:  # Did they pass
        if board.fp:
            board.eg = True
        else:
            board.fp = True
    else:
        #  motor.move(game_input)  # move to the space
        print("Putting Stone", move)
        remove_lst = board.update_game_arr(move, stone_type)
        board.fp = False
    if len(remove_lst) > 0:
        print("Removing: ", str(len(remove_lst)), "Nodes from board")
        # motor.multi_move(remove_lst)  # remove all the stones from the move


def parseScore(score):
    splitted = score.split("+")
    color = splitted[0]
    score = splitted[1]
    if color == "b":
        print("Black won with a score of ", score)
    else:
        print("White won with a score of ", score)


def gnugo_init():
    AI = pex.PopenSpawn("gnugo --mode gtp", encoding="utf-8")
    AI.sendline("boardsize 9")
    AI.sendline("clear_board")
    return AI


def main():
    # model = input("Choose, gnugo or leelazero")
    AI = gnugo_init()
    f_name = ""
    game_processor = Sgf_Process(9, f_name, AI)
    Player_Color = input("choose black or white")
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
            vertex = input(print_player_text)
            AI.sendline("play black {}".format(vertex))
            AI.expect("=")
            gLCL(vertex, game_processor, gtp.BLACK)
            print(game_processor)

        AI.sendline(command)  # Generate Move
        AI.expect("[\w]{6}|[A-Z]\d{1,2}")  # Get move
        AI_move = AI.after
        print("AI Moved to:", AI_move)
        if AI_move == gtp.RESIGN:
            print("AI has resigned you have won")
            break
        gLCL(AI_move, game_processor, AI_col)

        if Player_Color == "white":
            print(game_processor)
            vertex = input(print_player_text)
            AI.sendline("play white {}".format(vertex))
            gLCL(vertex, game_processor, gtp.WHITE)
            print(game_processor)

    print(game_processor)
    print("Game Has ended")
    AI.sendline("final_score")
    AI.expect("[\w][+]\d+[.]\d")
    score = AI.after
    parseScore(score)
    game_processor.create_sgf()
    print("Please find your game at ", game_processor.file_out_name)
    print("We hope you have had an fun time with out unqiue way with playing Go!!")
    AI.sendline("quit")  # End AI Instance
    print("Credits; Sean Lai, Andy Li, Ray Eu, Safhira Hack")


main()
