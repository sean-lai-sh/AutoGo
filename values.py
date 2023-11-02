import copy

# A LIST OF CONSTANTS USED FOR CODE
GNU_GO_PRESET = ["gnugo", "--mode", "gtp", "--level"]
SLEEP_CONST = 10


def gen_gnugo_preset():
    return GNU_GO_PRESET.copy()

