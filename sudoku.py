import time

"""
input_data = [
             [1, 4, 0,   0, 0, 0,     0, 0, 0],
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             [0, 0, 0,   0, 0, 0,     0, 0, 0],
             [0, 0, 0,   0, 0, 0,     0, 0, 0]
            ]
            
            
"""
input_data = [
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

def get_box(board, row, col):
    box_row = box_col = 0 # Index of top left pos in current box
    
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
    box = get_box(board, row, col)
    if digit in box:
        return False

    return True
    

def next_index(row, col):
    col = col + 1
    if col >= 9:
        col = 0
        row = row + 1
        
    return row, col

def prev_index(row, col):
    if col <= 0:
        col = 8
        row = row - 1
    else:
        col = col - 1
        
    return row, col

def bp():
    return

def solve_dat_shit(board, row, col, used_digits_at_index, predef_indicies):

    while True:
        print('Index: ' + str(row) + ", "  + str(col))
        #print_board(board)
        #time.sleep(0.50)
        bp()
        if (row, col) in predef_indicies:
            row, col = next_index(row, col)
            if row == 9: # Reached the end
                print('Solution found:')
                return board
        else:
            #if (row, col) in used_digits_at_index:
            #    if len(used_digits_at_index[(row, col)]) == 9:
            #        print('No solution found, len')
            #        return board
            digit_placed = False
            for digit in range(1, 10):
                if valid_digit(board, digit, row, col, used_digits_at_index):
                    board[row][col] = digit
                    if (row, col) in used_digits_at_index:
                        used_digits_at_index[(row, col)].append(digit)
                    else:
                        used_digits_at_index[(row, col)] = [digit]
                    row, col = next_index(row, col)
                    if row == 9: # Reached the end
                        print('Solution found:')
                        return board
                    digit_placed = True
                    break

            if not digit_placed:
                # Reached dead end, try to backtrack
                print('Backtracking at index: ' + str(row) + ", "  + str(col))
                #print_board(board)
                used_digits_at_index[(row, col)] = []
                board[row][col] = 0
                row, col = prev_index(row, col)
                while (row, col) in predef_indicies:
                    row, col = prev_index(row, col)
                if row == -1:
                    print('No solution found')
                    return board
            
    
def print_board(board):
    print('=================================')
    for index, row in enumerate(board):
        print('{} | {} | {}'.format(row[:3], row[3:6], row[6:9]))
        if (index + 1) % 3 == 0 and index < 7: # Fancy way of writing "if index == 2 or 5"
            print('---------------------------------')
    print('=================================')
    
def get_predefined_indicies(board):
    indicies = []
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] != 0:
                indicies.append((row, col))
    
    return indicies
            

if __name__ == '__main__':
    used_digits_at_index = {}
    predef_indicies = get_predefined_indicies(input_data)
    print_board(solve_dat_shit(input_data, 0, 0, used_digits_at_index, predef_indicies))
    
    
