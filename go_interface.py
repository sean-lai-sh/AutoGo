from gtp_initialize import GTPFacade
from gtp import gtp
import time
Sleep_Constant = 10


def start_player_vs_ai():
    # Query Input for mode
    AI_settings = ["gnugo", "--mode", "gtp", "--level", "10"]
    AI = GTPFacade("white", AI_settings)
    AI.boardsize(9)
    AI.komi(6.5)
    AI.clear_board()
    first_pass = False
    while True:
        player_vertex = get_vertex()  # TO Implement
        if player_vertex == gtp.PASS:
            if first_pass:
                break
            else:
                first_pass = True
        else:
            first_pass = False
        AI.play(gtp.BLACK, player_vertex)
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
            first_pass = False
        time.sleep(Sleep_Constant)

    final_score = AI.final_score()
    AI.close()
    # Query Input for other settings I.e Komi & what not
    # Init GnuGo
    # Start Game
    # End game when needed
    return final_score
