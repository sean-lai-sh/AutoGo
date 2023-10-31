from sgfmill import sgf


with open("test_file_archives/test_file_9x9.sgf", "rb") as f:
    game = sgf.Sgf_game.from_bytes(f.read())
winner = game.get_winner()
board_size = game.get_size()
root_node = game.get_root()
b_player = root_node.get("PB")
w_player = root_node.get("PW")
for node in game.get_main_sequence():
    print(node.get_move())
