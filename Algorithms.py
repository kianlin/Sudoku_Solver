
###########################################################################
############################## SUDOKU SOLVER ##############################
###########################################################################

##### PLANNING PROCESS #####
# Step 1: Input Grid with a 9 x 9 matrix
# Step 2: Check if a digit is valid based on certain constraints:
    # No same digit in the same row
    # No same digit in the same column
    # No same digit in the same box
    # All number appears a total of 9 times (constrain: count <= 9)
# Step 3: 
    # If isValid() = False, try the next digit in the same grid
    # If isValid() = True, fill that position with that digit, and move to the next grid
# Step 4: Recurve the process for the next grid. 
    # If all 9 digits fails, backtrack to the previous grid and get another digit to fill
    # Backtrack however far it needed. Move on to the next grid after getting the new digit.

import numpy as np
from io import StringIO

# Utility function: To create new grid board
def create_new():
    board = np.zeros((9,9), dtype=np.int32)
    return board

# Utility function: To convert string puzzle to grid board
def create_grid(board_in_string):
    cleaned = board_in_string.replace(".", "0").replace('\n','')
    num = list(map(int, cleaned))
    board = np.array(num).reshape(9,9)
    return board

# Utility function: To display grid board
def display_grid(board):
    board_mat = np.array(board)
    for i in range(board_mat.shape[0]): # rows
        for j in range(board_mat.shape[1]): # columns
            print(board_mat[i][j], end = " ")
        print()
    print("\n")


# Function: To check if a digit is valid to be filled on the board
def is_valid(board, digit, row, col):
    # Three constraints:
        # No same digit in the same row
        # No same digit in the same column
        # No same digit in the same box
        
    flag = True # Toggle to False if it fails any of the constraints
    
    board_mat = np.array(board)
    target_row = board_mat[row-1] # Get all the numbers in the row
    target_col = board_mat[:,col-1] # Get all the numbers in the column
    
    box_row_start =  (row - 1) - ((row - 1) % 3)
    box_col_start =  (col - 1) - ((col - 1) % 3)
    target_box = board_mat[box_row_start:box_row_start+3, box_col_start:box_col_start+3] # Get all the numbers in the box

    # Check if digit violates any of the constraints
    if (digit in target_row) | (digit in target_col) | any(digit in r for r in target_box):
        flag = False
    
    return flag


# Function: To identify the empty grids on the board using Boolean fields
def is_empty(board):
    board_mat = np.array(board)
    return (board_mat == 0)


# Function: To check if there is a next empty grid, and return its position if so. If all filled, return False
def next_empty(board, pos):
    empty_grid = np.array(is_empty(board))
    for row in range(empty_grid.shape[0]):
        for col in range(empty_grid.shape[1]):
            if (empty_grid[row][col] == True):
                pos[0] = row
                pos[1] = col
                return True # Empty grid still exists
    return False # All grids filled


# Function: To find a solution for a given board
def solve(board):
    # Traverse through the board from left to right, starting with [0, 0]
    # Check if there are empty grids. If no, means board has been solved and return True.
        # Else find the next empty grid to be filled
    # Check if digit is_valid() to be filled in this empty grid
        # If digit is_valid() == True
            # Assign the digit to this position. 
            # Recurse the function to see if this combination works. Returns True if board can be solved.
            # Else, set the position back to empty (i.e. 0), and try the next digit
        # If all digit checked and all are invalid, traverse back to the next digit
        
    # Start with row 0, col 0
    pos = [0, 0] 
    
    # Check if board filled (i.e. no empty grids), else, modify pos to suggest next empty grid
    if (not next_empty(board, pos)):
        print("Solved Board: \n")
        display_grid(board)
        return True
    
    # Current position to fill
    row = pos[0]
    col = pos[1]
    
    # Create new copy of board
    board_mat = np.array(board)
    
    for digit in range(1, 10):
        # Check if digit is_valid
        valid = is_valid(board_mat, digit, row+1, col+1)
        if valid:
            # Assign the digit to the curr pos
            board_mat[row][col] = digit
            
            # Recurse to see if the combination works
            if solve(board_mat):
                # print("Solved Board Stage 2: ")
                # display_grid(board_mat)
                return True
            
            # Solution fails, set it back to empty grid
            board_mat[row][col] = 0 
    
    return False
    
    
# Test: Test scripts to see if functions works
def test():
    test_input =    [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    
    testarr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    zero_arr = create_new()
    pos = [0, 0]
    
    test1 = is_valid(test_input, 4, 1, 2) == False # Same digit in the same row (Expected: False)
    test2 = is_valid(test_input, 1, 2, 5) == False # Same digit in the same col (Expected: False)
    test3 = is_valid(test_input, 7, 1, 2) == False # Same digit in the same box (Expected: False)
    test4 = is_valid(test_input, 4, 5, 3) == True # Valid answer (Expected: True)
    test5 = next_empty(testarr, pos) == False # Do not contain empty grids (Expected: False)
    test6 = next_empty(zero_arr, pos) == True # Contain empty grids (Expected: True)
    test7 = solve(test_input) == True # Solve for a solution (Expected: True)
    
    #  output_grid = "3 1 6 5 7 8 4 9 2"
    # "5 2 9 1 3 4 7 6 8"
    # "4 8 7 6 2 9 5 3 1"
    # "2 6 3 4 1 5 9 8 7"
    # "9 7 4 8 6 3 1 2 5"
    # "8 5 1 7 9 2 6 4 3"
    # "1 3 8 9 4 7 2 5 6"
    # "6 9 2 3 5 1 8 7 4"
    # "7 4 5 2 8 6 3 1 9"
    
    all_test = [test1, test2, test3, test4, test5, test6, test7]
    
    if False in all_test:
        print("Errors identified")
    else:
        print("All tests passed")


def main():
    if (solve(input_grid)):
        print("Solution exists!")
    else:
        print("\nNo solution exists")

if __name__== "__main__" :
    # Other Test Cases:
    # "974236158638591742125487936316754289742918563589362417867125394253649871491873625"
    # "3.542.81.4879.15.6.29.5637485.793.416132.8957.74.6528.2413.9.655.867.192.965124.8"
    # "2564891733746159829817234565932748617128.6549468591327635147298127958634849362715"
    
    start = "..2.3...8.....8....31.2.....6..5.27..1.....5.2.4.6..31....8.6.5.......13..531.4.."
    input_grid = create_grid(start)
    
    main()
    