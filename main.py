from sgfmill import sgf
from sgfmill import sgf_moves
from sgfmill import ascii_boards
from sgf_process import Sgf_process

from sgfmill import ascii_boards
# Reading game from bytes: TO CHANGE TO GAME FILE ONCE CODES READY
game_processing = Sgf_process()
### game_arr => interface with the motors
game = game_processing.game
game_arr = [[None for i in range(9)] for k in range(9)]
game_board, plays = sgf_moves.get_setup_and_moves(game)
print(ascii_boards.render_board(game_board))


### Writing a game file: upon input

