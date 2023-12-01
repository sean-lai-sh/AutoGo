import numpy as np
import serial
import time
from go_processing import from_gtp
class Motors:

    def __init__(self, start_pos = None, size = 9):
        self.start_pos = start_pos
        self.board_size = size
        # self.ser = serial.Serial('/dev/ttyACM0', 9600)
        # self.ser.reset_input_buffer()
        self.game_state = np.zeros((self.board_size + 1,self.board_size + 1))

    def get_user_input(self):
        res = input()
        return res    

    def create_path(self, end_pos):
        start_pos = self.start_pos
        path = []
        move = from_gtp(end_pos, self.board_size)
        moveX = move[0]
        moveY = move[1]
        while moveX < 0:
            path.append("U")
            moveX += 1
        while moveX > 0:
            path.append("D")
            moveX -= 1

        while moveY < 0:
            path.append("L")
            moveY += 1
        while moveY > 0:
            path.append("R")
            moveY -= 1
        return path

    def move(self, end_pos):
        p = self.create_path(end_pos)
        self.move_along_path(p)
        return 1
    def send_motor_instruction(self, direction):
        self.ser.reset_input_buffer()
        input_str = bytes(direction + "\n")
        self.ser.write(input_str)
        line = self.ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

    def close(self):
        self.ser.close()
    def move_along_path(self, path):
        for move in path:
            self.send_motor_instruction(move)

    def multi_move(self, lst_moves):
        # To be implemented @il.ydna
        pass

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

        # Create start and end node
        start_node = motors.Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = motors.Node(None, end)
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
                new_node = motors.Node(current_node, node_position)

                # Append
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


motors = Motors("A1")
print(motors.create_path("C9"))