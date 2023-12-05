import pexpect.popen_spawn as pex

# TODO SWAP TO pexpect


def sendcommand(gtp_instance: pex.PopenSpawn, command: str, args, expect_str="="):
    # TODO SWAP TO pex.spawn when porting to unix
    if args is None:
        send_str = command  # Used for certain commands like clearboard with no args
    else:
        send_str = command + " " + args  # Used for most commands
    print("Send_str:", send_str)
    gtp_instance.send(send_str)  # Send it to the subprocess
    gtp_instance.expect(expect_str)  # Let us know when subprocess has completed


def boardsize(gtp_instance, b_size):
    # Error Checking
    if not isinstance(b_size, int):
        raise Exception("Invalid response")
    elif b_size < 0 or b_size > 19:
        return Exception("Invalid range: boardsize should be 1-19 and an integer")
    sendcommand(gtp_instance, "boardsize", str(b_size))


def komi(gtp_instance, komi):
    if not komi.isdigit():
        raise Exception("Invalid input")
    sendcommand(gtp_instance, "komi", komi)


def clear_board(gtp_i):
    sendcommand(gtp_i, "clear_board", None)


def genmove(gtp_i, color):
    sendcommand(gtp_i, "genmove", color, expect_str="[A-Z]\d+")
    return gtp_i.after  # Get the coordinates identified through regex


def showboard(gtp_i):
    sendcommand(gtp_i, "showboard", None)


def play(gtp_instance, color, vertex):
    sendcommand(gtp_instance, "play " + color, vertex)


def final_score(gtp_instance):
    sendcommand(gtp_instance, "finalscore", None)


def close(gtp_instance):
    sendcommand(gtp_instance, "sendeof", None)


# GNUGO = ["gnugo", "--mode", "gtp"]
# GNUGO_LEVEL_ONE = ["gnugo.exe", "--mode", "gtp", "--level", "1"]
# GNUGO_MONTE_CARLO = ["gnugo.exe", "--mode", "gtp", "--monte-carlo"]
#
#
#
#
# black = GTPFacade("black", GNUGO)
# white = GTPFacade("white", GNUGO)
#
#
# black.boardsize(9)
# white.boardsize(9)

# black.komi(5.5)
# white.komi(5.5)
#
# black.clear_board()
# white.clear_board()
#
# first_pass = False
# print("Works")
# while True:
#     vertex = black.genmove(gtp.BLACK)
#     if vertex == gtp.PASS:
#         if first_pass:
#             break
#         else:
#             first_pass = True
#     else:
#         first_pass = False
#
#     black.showboard()
#
#     white.play(gtp.BLACK, vertex)
#     white.showboard()
#
#     vertex = white.genmove(gtp.WHITE)
#     if vertex == gtp.PASS:
#         if first_pass:
#             break
#         else:
#             first_pass = True
#     else:
#         first_pass = False
#
#     white.showboard()
#
#     black.play(gtp.WHITE, vertex)
#     black.showboard()
#
# black.final_score()
# white.final_score()
#
# black.close()
# white.close()
