from sgfmill import sgf

game = sgf.Sgf_game.from_bytes(
    b"(;FF[4]GM[1]SZ[9]CA[UTF-8];B[ee];W[ge])",
    override_encoding="iso8859-1")

print(game.get_size())
game_arr = [[None for i in range(9)] for k in range(9)]
for node in game.get_main_sequence():
    node_data = node.get_move()
    if node_data == (None, None):
        continue
    row_val = node_data[1][0]
    col_val = node_data[1][1]
    game_arr[row_val][col_val] = node_data[0]


for k in range(len(game_arr)):
    for j in range(len(game_arr[k])):
        print(game_arr[k][j] , end= " ")
    print()



