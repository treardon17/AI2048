"""
2048 Game Clone
By George Siatras   GitHub: gsiatras
https://github.com/gsiatras/2048

We slightly modified it
"""

#mport poc_2048_gui
from random import randrange
from random import random
import numpy as np

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
OFFSETS = {'up': (1, 0), 'down': (-1, 0), 'left': (0, 1), 'right': (0, -1)}





class TwentyFortyEight:
    """
    Class to run the game
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._is_occupied = False
        self._is_changed = False
        self.reset()
        self.score = 0
    
    
    def reset(self):
        """
        Reset the game so the grid is empty
        """        
        self._grid = [[0 for this_col in range(self._grid_width)] for this_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
            
    def __str__(self):
        """
        Return a string representation of the grid
        """        
        return str(self._grid)

    def merge(self, line):
        """
        Function that merges a single row or column in 2048
        """
        length = len(line)
        result = [0] * length
        last_index = 0

        for current_index in range(length):
            if line[current_index] != 0:
                result[last_index] = line[current_index]
                last_index += 1

        for key in range(length - 1):
            if result[key] is result[key + 1]:
                result[key] = result[key] * 2
                self.score += result[key]
                result.pop(key + 1)
                result.append(0)

        return result


    def get_grid_height(self):
        """
        Get the height of the board
        """
        return self._grid_height
    
    
    def get_grid_width(self):
        """
        Get the width of the board
        """                
        return self._grid_width
                            

    def move(self, action):
        """
        Move all tiles in the given direction and add a new tile if any tiles moved
        """
        offset = OFFSETS[action]
        temp_grid = []
            
        # Up
        if action == 'up':
            for row in range(self._grid_width):
                start = 0
                temp_list = []
                for this_col in range(self._grid_height):
                    temp_list.append(self._grid[start][row])
                    start += offset[0]
                temp_list = self.merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[col][row]
        
        # Down
        elif action == 'down':
            for row in range(self._grid_width):
                start = self._grid_height -1
                temp_list = []
                for this_col in range(self._grid_height):
                    temp_list.append(self._grid[start][row])
                    start += offset[0]
                temp_list = self.merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[col][self._grid_height -1 -row]
        
        # Left
        elif action == 'left':
            for col in range(self._grid_height):
                start = 0
                temp_list = []
                for this_row in range(self._grid_width):
                    temp_list.append(self._grid[col][start])
                    start += offset[1]
                temp_list = self.merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[row][col]
                    
        # Right                    
        elif action == 'right':
            for col in range(self._grid_height):
                start = self._grid_width -1
                temp_list = []
                for this_row in range(self._grid_width):
                    temp_list.append(self._grid[col][start])
                    start += offset[1]
                temp_list = self.merge(temp_list)
                temp_grid.append(temp_list)
            for row in range(self._grid_height):
                for col in range(self._grid_width):
                    self._grid[row][col] = temp_grid[row][self._grid_width -1 -col]
        
        total_num = 1
        for value in self._grid:
            for val_el in value:
                total_num *= val_el
                if total_num == 0:
                    self._is_occupied = False
                    break
                else:
                    self._is_occupied = True
                    
        if self._is_changed or not self._is_occupied:
            self.new_tile()
            self._is_change = False
        
            
    def new_tile(self):
        """
        Create a new tile
        """              
        probabilities = []
        for this_i in range(100):
            if this_i < 90:
                probabilities.append(2)
            else:
                probabilities.append(4)                      
        while True :
            random_row = randrange(0, self._grid_height)
            random_col = randrange(0, self._grid_width)
            if self._grid[random_row][random_col] is 0 :
                self.set_tile(random_row, random_col, probabilities[int(random() * 100)])
                break
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position [row][col] to the given value
        """
        self._grid[row][col] = value


    def get_tile(self, row, col):
        """
        Return the value of the tile at position [row][col]
        """          
        return self._grid[row][col]


    def printBoard(self):
        #os.system("cls")
        for x in self._grid:
            for y in x:
                print '{0:3}'.format(y),
            print
        print "-------------------"
        print "[+] Score:", self.score

    def getGameState(self):
        return np.array(self._grid)

    def getScore(self):
        return self.score

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))