from sgfmill import sgf
from sgfmill import sgf_board_interface

class Sgf_process:
    def __init__(self, file_extension="test_file_archives/test_file_9x9.sgf"):
        ### Read the file
        with open(file_extension, "rb") as f:
            self.game = sgf.Sgf_game.from_bytes(f.read())
        f.close()



    def remove_stone_path(self, array, sgf):
        """
        :param array:
        :param sgf:
        :return: linked list or ordered list of paths to remove stones from current location of removing stone tool
        """

    def move_stone_path(self, array, sgf):
        pass

    def identify(self):
        pass
