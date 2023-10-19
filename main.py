from sgfmill import sgf

game = sgf.Sgf_game.from_bytes(
    b"(;FF[4]GM[1]SZ[9]CA[UTF-8];B[ee];W[ge])",
    override_encoding="iso8859-1")

print(game.get_size())

for node in game.get_main_sequence():
    print(node.get_move())

