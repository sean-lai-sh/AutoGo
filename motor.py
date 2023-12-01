import numpy as np
import serial
import time
import gtp
from go_processing import from_gtp
class Motors:

    def __init__(self, game_processor, ai_color, player_color, board_size = 9, start_pos = (0,0)):
        self.current_pos = start_pos
        self.board_size = board_size
        self.ser = serial.Serial('/dev/ttyACM1', 9600)
        self.ser.reset_input_buffer()

        self.game_state = np.zeros((self.board_size + 1,self.board_size + 1))
        self.piece_start = (9, 9)
        self.black_cap = (0, 9)
        self.white_cap = (9, 0)

    def send_motor_instruction(self, direction):
        ser.write(direction.encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

    def close(self):
        self.ser.close()

    class Node():
        """A node class for A* Pathfinding"""

        def __init__(self, parent=None, position=None):
            self.parent = parent
            self.position = position

            self.g = 0
            self.h = 0
            self.f = 0

        def __eq__(self, other):
            return self.position == other.position

    def astar(self, maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""
        #print(maze)
        # Create start and end node
        start_node = Motors.Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Motors.Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Motors.Node(current_node, node_position)

                # Append
                #print(new_node.position)
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                            (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)
        print("astar done")
    def translate_astar(self, astar_lst):
        res_lst = []
        for move in astar_lst:
            if move == (1, 0):
                res_lst.append("R.")
            if move == (-1, 0):
                res_lst.append("L.")
            if move == (0, 1):
                res_lst.append("U.")
            if move == (0, -1):
                res_lst.append("D.")
        return res_lst

    def move_through_list(self, lst):
        for step in lst:
            self.send_motor_instruction(step)

    def pickup(self, end_pos):
        #TODO: magnet off
        print("reached pickup call")
        move_lst = self.astar(self.game_state, self.current_pos, self.piece_start)
        print(move_lst)
        move_lst = self.translate_astar(move_lst)
        print(move_lst)
        self.move_through_list(move_lst)
        #TODO: magnet on
        self.current_pos = self.piece_start
        move_lst = self.translate_astar(self.astar(self.game_state, self.current_pos, end_pos))
        self.move_through_list(move_lst)
        #TODO: magnet off


    def dropoff(self, start_pos, color):
        if color == gtp.BLACK:
            end_pos = self.black_cap
        else:
            end_pos = self.white_cap
        #TODO: magnet off
        move_lst = self.translate_astar(self.astar(self.game_state, self.current_pos, start_pos))
        self.current_pos = start_pos
        self.move_through_list(move_lst)
        # TODO: magnet on
        move_lst = self.translate_astar(self.astar(self.game_state, self.current_pos, end_pos))
        self.current_pos = end_pos
        # TODO: magnet off


    def move(self, end_pos, move_color):
        self.pickup(end_pos)
    def multi_move(self, lst_moves, move_color):
        for moves in lst_moves:
            self.dropoff(moves, move_color)






