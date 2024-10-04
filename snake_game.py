from collections import deque
from enum import Enum
import os

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class GameBoard:
    def __init__(self, size, has_boundary) -> None:
        self.size = size
        self.has_boundary = has_boundary
        self.blocks = set() # set of all the blocked cells
        self._initBlocks()
    
    def _initBlocks(self):
        # filling blocks with boundary cells
        for i in range(self.size):
            self.blocks.add((0, i))
            self.blocks.add((i, 0))
            self.blocks.add((self.size-1, i))
            self.blocks.add((i, self.size-1))


class Snake:
    def __init__(self) -> None:
        self.body = deque()
        self.body_cells = set()
        self.initBody() #to set snake's initial position and structure
        self.direction = Direction.RIGHT
    
    def initBody(self, row=5, col=3, size=4):
        for i in range(size):
            self.body.append((row, col+i))



class SnakeGame:
    # gameboard = GameBoard()
    # snake = Snake()
    def __init__(self) -> None:
        self.snake = Snake()
        self.board = GameBoard(10, True)
        self.score = 0
        self.food = (3,4)

    def getNextLocationandDirection(self, input_direction : str): 
        '''
        x, y    head = x facing right
        Right -> x + 1, y
        Up -> x, y + 1
        Down -> x , y - 1;
        Left -> no changes
        direction U, D, R, L
        cd = 'R', i/p = 'U', cd = 'U' (x + 1, y)
        cd = 'R', i/p = 'D', cd = 'D' (x - 1, y)
        cd = 'R', i/p = 'R', cd = 'R'
        cd = 'R', i/p = 'L', cd = 'R'
        
        cd = 'L', i/p = 'U', cd = 'U'
        cd = 'L', i/p = 'D', cd = 'D'
        cd = 'L', i/p = 'R', cd = 'L'
        cd = 'L', i/p = 'L', cd = 'L'
        
        cd = 'U', i/p = 'U', cd = 'U'
        cd = 'U', i/p = 'D', cd = 'U'
        cd = 'U', i/p = 'R', cd = 'R'
        cd = 'U', i/p = 'L', cd = 'L'
        
        cd = 'D', i/p = 'U', cd = 'D'
        cd = 'D', i/p = 'D', cd = 'D'
        cd = 'D', i/p = 'R', cd = 'R'
        cd = 'D', i/p = 'L', cd = 'L'
        '''
        head = self.snake.body[-1]
        current_direction = self.snake.direction
        new_direction = current_direction
        new_location = head

        if input_direction == 'D':
            if new_direction in (Direction.UP, Direction.DOWN, Direction.RIGHT):
                new_location = (head[0], head[1] + 1)
                new_direction = Direction.RIGHT
            elif new_direction is (Direction.LEFT):
                new_location = (head[0], head[1] - 1)
                new_direction = Direction.LEFT

        elif input_direction == 'A':
            if new_direction in (Direction.UP, Direction.DOWN, Direction.LEFT):
                new_location = (head[0], head[1] - 1)
                new_direction = Direction.LEFT
            elif new_direction is (Direction.RIGHT):
                new_location = (head[0], head[1] + 1)
                new_direction = Direction.RIGHT

        elif input_direction == 'W':
            if current_direction in (Direction.RIGHT, Direction.LEFT, Direction.UP) :
                new_location = (head[0] - 1, head[1])
                new_direction = Direction.UP
            elif current_direction in (Direction.DOWN) :
                new_location = (head[0] + 1, head[1])
                new_direction = Direction.DOWN

        elif input_direction == 'S':
            if new_direction in (Direction.RIGHT, Direction.LEFT, Direction.DOWN) :
                new_location = (head[0] + 1, head[1])
                new_direction = Direction.DOWN
            elif new_direction in (Direction.UP) :
                new_location = (head[0] - 1, head[1])
                new_direction = Direction.UP


        return new_location, new_direction

    def isSafePosition(self, new_position) -> bool:
        # check if the new_position is on blocks
        if new_position in self.board.blocks:
            return False
        # check if the new_position is on snake body
        if new_position in self.snake.body and new_position != self.snake.body[0]:
            return False
        return True

    def move(self, input_direction : str) -> bool:

        new_position, new_direction = self.getNextLocationandDirection(input_direction)
        if not self.isSafePosition(new_position):
            # snake collided with something
            return False
        self.snake.body.append(new_position)
        self.snake.direction = new_direction
        self.snake.body.popleft()

        return True


    def display(self, is_game_over:bool):
        cls()
        print('\n\n\n\n')
        for i in range(self.board.size):
            for j in range(self.board.size):
                if (i, j) in self.board.blocks or (i, j) in self.snake.body or (i, j) == self.food:
                    if ((i, j) == self.snake.body[-1]):
                        print('*', end = "")
                    else:
                        print('#', end = "")
                else:
                    print(' ',end = "")
            print()
        print('\n\n\n')

    def play(self):
        # initialize snake, food, board
        self.display(False)
        print('Enter\nW for UP\nS for DOWN\nA for LEFT\nD for RIGHT')
        while(True):
            direction = input()
            is_valid_move = self.move(direction) 
            self.display(is_valid_move)
            if not is_valid_move:
                break

snake_game = SnakeGame()
snake_game.play()
     
