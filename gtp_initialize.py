from subprocess import Popen, PIPE
from gtp import gtp


class GTPSubProcess(object):

    def __init__(self, label, args):
        self.label = label
        self.subprocess = Popen(args, stdin=PIPE, stdout=PIPE)
        print("{} subprocess created".format(label))

    def send(self, data):
        print("sending {}: {}".format(self.label, data))
        self.subprocess.stdin.write(data)
        result = ""
        while True:
            data = self.subprocess.stdout.readline()
            if not data.strip():
                break
            result += data
        print("got: {}".format(result))
        return result

    def close(self):
        print("quitting {} subprocess".format(self.label))
        self.subprocess.communicate("quit\n")


class GTPFacade(object):

    def __init__(self, label, args):
        self.label = label
        self.gtp_subprocess = GTPSubProcess(label, args)

    def name(self):
        self.gtp_subprocess.send("name\n")

    def version(self):
        self.gtp_subprocess.send("version\n")

    def boardsize(self, boardsize):
        self.gtp_subprocess.send("boardsize {}\n".format(boardsize))

    def komi(self, komi):
        self.gtp_subprocess.send("komi {}\n".format(komi))

    def clear_board(self):
        self.gtp_subprocess.send("clear_board\n")

    def genmove(self, color):
        message = self.gtp_subprocess.send(
            "genmove {}\n".format(gtp.gtp_color(color)))
        assert message[0] == "="
        return gtp.parse_vertex(message[1:].strip())

    def showboard(self):
        self.gtp_subprocess.send("showboard\n")

    def play(self, color, vertex):
        self.gtp_subprocess.send("play {}\n".format(gtp.gtp_move(color, vertex)))

    def final_score(self):
        self.gtp_subprocess.send("final_score\n")

    def close(self):
        self.gtp_subprocess.close()


GNUGO = ["gnugo", "--mode", "gtp"]
GNUGO_LEVEL_ONE = ["gnugo", "--mode", "gtp", "--level", "1"]
GNUGO_MONTE_CARLO = ["gnugo", "--mode", "gtp", "--monte-carlo"]


black = GTPFacade("black", GNUGO)
white = GTPFacade("white", GNUGO_LEVEL_ONE)

black.name()
black.version()

white.name()
white.version()

black.boardsize(9)
white.boardsize(9)

black.komi(5.5)
white.komi(5.5)

black.clear_board()
white.clear_board()

first_pass = False

while True:
    vertex = black.genmove(gtp.BLACK)
    if vertex == gtp.PASS:
        if first_pass:
            break
        else:
            first_pass = True
    else:
        first_pass = False

    black.showboard()

    white.play(gtp.BLACK, vertex)
    white.showboard()

    vertex = white.genmove(gtp.WHITE)
    if vertex == gtp.PASS:
        if first_pass:
            break
        else:
            first_pass = True
    else:
        first_pass = False

    white.showboard()

    black.play(gtp.WHITE, vertex)
    black.showboard()

black.final_score()
white.final_score()

black.close()
white.close()
