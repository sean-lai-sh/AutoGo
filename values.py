import copy
from enum import IntEnum
# A LIST OF CONSTANTS USED FOR CODE
GNU_GO_PRESET = ["gnugo", "--mode", "gtp", "--level"]
LEELAZERO_PRESET = ["leelaz", "--gtp", "-w", "40b.gz", "--noponder", "-p", "3200"]
SABAKI_PATH = "" # TO ADD
SLEEP_CONST = 10
USE_CONSOLE = False


def gen_gnugo_preset():
    return "gnugo --mode -- gtp"


def gen_leelazero_preset():
    return LEELAZERO_PRESET

def S_PATH():
    return SABAKI_PATH
