"""
#   A simple Sudoku solver.
#   
#   Starting from the top left and moving column by column, it inserts digits accepted by the rules.
#   If it can't palce a digit, it backtracks and blacklists the previous digit at that specific index
#   and tries a new one. This reoccurs until the Sudoku is solved.
"""
import copy

ANIMATION_MODE = 0 # 1 to animate (slow), 0 to only show solution (fast)
if ANIMATION_MODE:
    import time
    import os

input_sudoku = [
             [0, 0, 0,   9, 0, 0,     6, 0, 0],
             [6, 4, 0,   0, 0, 0,     0, 3, 1],
             [8, 0, 0,   0, 1, 0,     0, 0, 9],
             
             [0, 0, 5,   0, 2, 0,     0, 0, 0],
             [9, 0, 0,   0, 7, 0,     0, 1, 5],
             [0, 7, 4,   0, 0, 0,     9, 2, 0],
             
             [0, 0, 6,   8, 3, 0,     0, 5, 7],
             [0, 1, 0,   0, 0, 0,     0, 9, 6],
             [0, 5, 0,   0, 9, 0,     2, 0, 0]
            ]

# Returns a list of all digits in a box. A box is a 3x3 field containing row, col.
def get_box_digits(board, row, col):
    # Index of top left pos in current box
    box_row = box_col = 0
    
    # Find the index of the box containing row, col.
    if row <= 2:
        box_row = 0
    elif row > 2 and row <= 5:
        box_row = 3
    else:
        box_row = 6
        
    if col <= 2:
        box_col = 0
    elif col > 2 and col <= 5:
        box_col = 3
    else:
        box_col = 6
        
    # Get digits in box
    digits = []
    for row_index in range(box_row, box_row + 3):
        for col_index in range(box_col, box_col + 3):
            digits.append(board[row_index][col_index])
            
    return digits

# Returns true if @param digit can be placed at @param row, @param col>.
def valid_digit(board, digit, row, col, used_digits_at_index):
    if (row, col) in used_digits_at_index:
        if digit in used_digits_at_index[(row, col)]:
            return False
            
    # Check row
    if digit in board[row]:
        return False
        
    # Check col
    for i in range(0, 9):
        if board[i][col] == digit:
            return False
            
    # Check 3x3 box
    box = get_box_digits(board, row, col)
    if digit in box:
        return False

    return True
    
# Increments row and col to point at the next index on the board.
def next_index(row, col):
    col = col + 1
    if col >= 9:
        col = 0
        row = row + 1
        
    return row, col

# Decrements row and col to point at the previous index on the board.
def prev_index(row, col):
    if col <= 0:
        col = 8
        row = row - 1
    else:
        col = col - 1
        
    return row, col

# Terminal animation
def animate_solution(board, row, col):
    time.sleep(0.002)
    os.system('clear')
    print('Index: ' + str(row) + ", "  + str(col))
    print_board(board)

# Prints the Sudoku in a presentable way
def print_board(board):
    print('=================================')
    for index, row in enumerate(board):
        print('{} | {} | {}'.format(row[:3], row[3:6], row[6:9]))
        if (index + 1) % 3 == 0 and index < 7: # Fancy way of writing "if index == 2 or 5"
            print('---------------------------------')
    print('=================================')
    
# Returns a list of indicies containing a non zero digit.
def get_predefined_digit_indicies(board):
    indicies = []
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] != 0:
                indicies.append((row, col))

                # Following is a hacky solution to check if the input Sudoku is valid.
                # Just ignore it.
                board_without_current_index = copy.deepcopy(board)
                board_without_current_index[row][col] = 0
                if not valid_digit(board_without_current_index, board[row][col], row, col, {}):
                    print("Illegal input Sudoku, unsolvable.")
                    exit(0)
    
    return indicies

# Attempts to solve the Sudoku given by board.
def solve_dat_shit(board, predef_indicies):
    # Current index
    row = col = 0
    # Keeps track of all digits that has tried to be placed and is placed at the given index.
    # Useful for backtracking and not getting stuck in an endless loop while trying the same
    # digit over and over again.
    used_digits_at_index = {}

    while True:
        if ANIMATION_MODE:
            animate_solution(board, row, col)

        # Skip index that can't be changed.
        if (row, col) in predef_indicies:
            row, col = next_index(row, col)
            if row == 9:
                print('Solution found:')
                return board

        # Try to insert a digit at current index, otherwise backtrack.
        else:
            digit_placed = False
            for digit in range(1, 10):
                if valid_digit(board, digit, row, col, used_digits_at_index):
                    board[row][col] = digit
                    if (row, col) in used_digits_at_index:
                        used_digits_at_index[(row, col)].append(digit)
                    else:
                        used_digits_at_index[(row, col)] = [digit]
                    row, col = next_index(row, col)
                    if row == 9:
                        if ANIMATION_MODE:
                            os.system('clear')
                        print('Solution found:')
                        return board
                    digit_placed = True
                    break
                
            # No digit could be placed, try to backtrack.
            if not digit_placed:
                if ANIMATION_MODE:
                    print('Backtracking at index: ' + str(row) + ", "  + str(col))
                #print_board(board)
                used_digits_at_index[(row, col)] = []
                board[row][col] = 0
                row, col = prev_index(row, col)
                while (row, col) in predef_indicies:
                    row, col = prev_index(row, col)
            

if __name__ == '__main__':
    predef_indicies = get_predefined_digit_indicies(input_sudoku)
    print_board(solve_dat_shit(input_sudoku, predef_indicies))
    
    
