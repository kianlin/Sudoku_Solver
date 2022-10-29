
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

input_grid =    [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                [5, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 7, 0, 0, 0, 0, 3, 1],
                [0, 0, 3, 0, 1, 0, 0, 8, 0],
                [9, 0, 0, 8, 6, 3, 0, 0, 5],
                [0, 5, 0, 0, 9, 0, 6, 0, 0],
                [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 7, 4],
                [0, 0, 5, 2, 0, 6, 3, 0, 0]]

order = np.arange(1, 10).reshape(3,3)


# Utility function: To create new grid board
def createNew():
    board = np.zeros((9,9), dtype=np.int32)
    return board


# Utility function: To display grid board
def displayGrid(board):
    board_mat = np.array(board)
    for i in range(board_mat.shape[0]): # rows
        for j in range(board_mat.shape[1]): # columns
            print(board_mat[i][j], end = " ")
        print()


# Function: To check if a digit is valid to be filled on the board
def isValid(board, digit, row, col):
    # Three constraints:
        # No same digit in the same row
        # No same digit in the same column
        # No same digit in the same box
        
    flag = True # Toggle to False if it fails any of the constraints
    
    board_mat = np.array(board)
    target_row = board_mat[row-1] # Get all the numbers in the row
    target_col = board_mat[:,col-1] # Get all the numbers in the column
    box_row = []
    box_col =[]
    
    for arr in order:
        if row in arr:
            box_row = arr
        if col in arr:
            box_col = arr
    
    target_box = board_mat[box_row[0]-1:box_row[-1], box_col[0]-1:box_col[-1]]
    
    # Check if digit violates any of the constraints
    if (digit in target_row) | (digit in target_col) | any(digit in r for r in target_box):
        flag = False
    
    return flag


# Test: Test scripts to see if functions works
def test():
    
    # Same digit in the same row (Expected: False)
    print("Insert 4 into row 1, col 2 is Invalid: " , isValid(input_grid, 4, 1, 2) == False) 
    
    # Same digit in the same col (Expected: False)
    print("Insert 1 into row 2, col 5 is Invalid: " , isValid(input_grid, 1, 2, 5) == False) 
    
    # Same digit in the same box (Expected: False)
    print("Insert 7 into row 1, col 2 is Invalid: " , isValid(input_grid, 7, 1, 2) == False) 
    
    # Valid answer (Expected: True)
    print("Insert 4 into row 5, col 3 is Valid: " , isValid(input_grid, 4, 5, 3) == True) 

test()

# Output Grid:
# 3 1 6 5 7 8 4 9 2
# 5 2 9 1 3 4 7 6 8
# 4 8 7 6 2 9 5 3 1
# 2 6 3 4 1 5 9 8 7
# 9 7 4 8 6 3 1 2 5
# 8 5 1 7 9 2 6 4 3
# 1 3 8 9 4 7 2 5 6
# 6 9 2 3 5 1 8 7 4
# 7 4 5 2 8 6 3 1 9