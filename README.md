# AutoGo AI Go Board

An automatic go board to allow people to interact with current cutting edge Go AI agents on a physical board.
Designed in mind for increasing accessibility to the game, with beginners and those with Alzheimer in mind. 

## Problem Context

[Go](https://en.wikipedia.org/wiki/Go_(game)), 
an ancient 3000 year-old chinese board game, has been traditionally very hard to get into as a 
casual player, with enigmatic "life or death" question books or expensive tutors as the only 
option to learn these rules. 
With the advent of [AlphaGo beating Lee Sedol, the best Go player in 2016](https://en.wikipedia.org/wiki/AlphaGo_versus_Lee_Sedol), 
this opened the flood gates for AI to become suitable mentors and aid in analyzing a players mistakes to help them improve. 
AutoGo attempts to bridge the traditionally digital format that may be hard for certain demographics due to language barriers, 
lack of experience, or cognitive disabilities. 
Through a physical board, we simplify the process in which new players need to play against a calibrated opponent matching their skill level. 
This also has an effect of improving their memory abilities which is shown to improve [early stage Alzheimer's patients](https://www.apa.org/news/press/releases/2002/10/memory-training)


## Constraints

- ### $100 credit with materials only from Amazon Prime
- ### Note: Additional 50$ used for replacement motors as part of a grant recieved in the second round of building

## Compilers/ Builders:

### [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/downloads/)

### [Cmake](https://cmake.org/)

### [Node](https://nodejs.org/en)

## Packages Used & Installation:
Language Vers[README.md](README.md)ions:
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
To install GNUGo and KataGo, please follow their documentation for debugging their installation process. Once setup please ensure that the built model is in the same directory as the go_interface script to avoid file not found errors.
Please also change the TODO if you are using a linux based Distribution as pexpect uses a different class to have the same functionality for devices on Windows.

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


