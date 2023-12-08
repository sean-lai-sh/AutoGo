# AutoGo AI Go Board

An automatic go board to allow people to interact with
## Constraints

- ### $100 credit with materials only from Amazon Prime

## Compilers/ Builders:

### [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/downloads/)

### [Cmake](https://cmake.org/)

### [Node](https://nodejs.org/en)

## Packages Used:
Language Versions:
- #### Python 3.11
- #### NodeJS 20.10.0 LTS

Install Python Dependencies
````commandline
pip install numpy
pip install sgfmill
pip install pyserial
pip install pexpect
pip install AppOpener
pip install tk
````

# Examples:

View below file for how it was implemented in the project. == [go_interface.py](https://github.com/sean-lai-sh/AutoGo/blob/main/go_interface.py) ==


# Documentation:

### go_interface:

>Start a coroutine to run a game with an AI and interface with a physical board.
Ends when game has two consecutive passes.


### Sgf_process(board_size, file_name, AI_reference):

>Constructor Method

#### Notes

- board_size: Int from 0 to 19 determining the square parameters ued to play Go
- file_name: name the file to output an SGF file when different method is called upon
- AI_reference: A GTPFacade instance. May or may not be deprecated by final version.

#### update_game_arr(self, gtp_vertex, TYPE: Stone_type):

> Add game data to a Matrix, update our game steps to an SGF builder, and return a list of indicies used to remove the stones.

Notes
- gtp_vertex: Formatted to GTP vertex standards
- TYPE: A Stone_type enum value (Black or White)

#### isValid(coord):

> Given Row and col Data in a tuple or list, check if the given row col combination is valid.

#### std_remove(color: Stone_type, coords):

> performs a usual removal operation using std_check function. Will return a tuple of data in format (int, list)

#### remove(color:Stone_type, coord, to_check):

> performs the remove operation over a more specified range of values, used in a recursion algoritm to check whether a group of stones must be removed


