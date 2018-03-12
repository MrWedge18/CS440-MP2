import numpy as np
import random
from math import pow
from sys import maxint
import pdb


board = np.zeros((7, 7))        # Actual state of the board. 0 = empty, 1 = red, 2 = blue
base = 5                        # For evaluation function. Explained later
nodes_expanded = 0

# State representation
# parent - not used, but already used a lot, and we're too lazy to go and remove it from every call
# board  - state of the board at the (potential) move
# player - 1 = red, 2 = blue
# piece  - x, y coordinates of piece placed
class Node:
    def __init__(self, parent, board, player, piece):
        self.parent = parent
        self.board = np.copy(board)
        self.piece = piece
        if piece is not None:
            self.board[piece[0]][piece[1]] = player

# Places one piece according to alpha beta search
# Player - 1 = red, 2 = blue
# Returns:
#   0 - There was a win
#   1 - There was no win
#  -1 - There can never be a win (Aka, agent can't make any winning moves)
def alpha_beta_place_piece(player):
    node = Node(None, board, player, None)                      # Initial node. Just the current state of the board
    tup = alpha_beta(node, 0, player, -maxint - 1, maxint)
    if tup[0] is not None:
        piece = tup[1]
    else:
        return -1
    board[piece[0]][piece[1]] = player

    # Check if there's five in a row
    curr = (7, 7)
    for x in range(7):
        for y in range(7):
            new = find_chains(player, 5, (x, y), curr, True)
            if new != curr:
                return 0

    return 1

# The alpha beta search
# node  - current node
# depth - current depth (0 - 3)
def alpha_beta(node, depth, player, alpha, beta):
    global nodes_expanded
    if depth == 3:      # At depth 3, return value of board
        p = 1
        if player == 1: # At depth 3, player is the opponent number. Switch it back
            p = 2

        return (eva(node.board, p), None)

    opponent = 1
    if player == 1:
        opponent = 2

    # Max
    if depth == 0 or depth == 2:
        best_value = -maxint - 1            # Minimum int
        best_move = None
        for x in range(7):
            for y in range(7):
                if node.board[x][y] == 0:                                   # Only place piece if blank
                    n = Node(node, node.board, player, (x, y))              # Places potential piece
                    v = alpha_beta(n, depth + 1, opponent, alpha, beta)     # Recurse

                    nodes_expanded += 1

                    if v[0] > best_value:                                   # Updates best value
                        best_value = v[0]
                        best_move = (x, y)

                    if best_value > alpha:                                  # Updates alpha
                        alpha = best_value

                    if best_value > beta:                                   # Check against beta
                        beta = best_value
                        return (best_value, best_move)

        return (best_value, best_move)

    # Min, pretty much the same as alpha
    else:
        best_value = maxint
        best_move = None
        for x in range(7):
            for y in range(7):
                if node.board[x][y] == 0:
                    n = Node(node, node.board, player, (x, y))
                    v = alpha_beta(n, depth + 1, opponent, alpha, beta)
                    nodes_expanded += 1
                    if v[0] < best_value:
                        best_value = v[0]
                        best_move = (x, y)

                    if best_value < beta:
                        beta = best_value

                    if best_value < alpha:
                        alpha = best_value
                        return (best_value, best_move)

        return (best_value, best_move)


# Places one piece according to minimax search
# Player - 1 = red, 2 = blue
# Returns:
#   0 - There was a win
#   1 - There was no win
#  -1 - There can never be a win (Aka, agent can't make any winning moves)
def minimax_place_piece(player):
    node = Node(None, board, player, None)
    tup = minimax(node, 0, player)
    if tup[0] is not None:
        piece = tup[1]
    else:
        return -1
    board[piece[0]][piece[1]] = player

    curr = (7, 7)
    for x in range(7):
        for y in range(7):
            new = find_chains(player, 5, (x, y), curr, True)
            if new != curr:
                return 0

    return 1

# The same as alpha beta. Just no alpha or beta
def minimax(node, depth, player):
    global nodes_expanded
    if depth == 3:
        p = 1
        if player == 1:
            p = 2
        #pdb.set_trace() 
        return (eva(node.board, p), None)

    opponent = 1
    if player == 1:
        opponent = 2

    # Max
    if depth == 0 or depth == 2:
        best_value = -maxint - 1
        best_move = None
        for x in range(7):
            for y in range(7):
                if node.board[x][y] == 0:
                    n = Node(node, node.board, player, (x, y))
                    v = minimax(n, depth + 1, opponent)
                    nodes_expanded += 1
                    if v[0] > best_value:
                        best_value = v[0]
                        best_move = (x, y)

       #if depth == 0:
        return (best_value, best_move)

    # Min
    else:
        best_value = maxint
        best_move = None
        for x in range(7):
            for y in range(7):
                if node.board[x][y] == 0:
                    n = Node(node, node.board, player, (x, y))
                    v = minimax(n, depth + 1, opponent)
                    nodes_expanded += 1
                    if v[0] < best_value:
                        best_value = v[0]
                        best_move = (x, y)

        return (best_value, best_move)

# Evaluation function
# checks for winning blocks and weights them exponentially based on how many of the player's pieces are in that block
def eva(node_board, player):
    value = 0
    opponent = 1

    if player == 1:
        opponent = 2

    for x in range(7):
        for y in range(7):
            hor = ((-1, -1), -1)
            ver = ((-1, -1), -1)
            sow = ((-1, -1), -1)
            now = ((-1, -1), -1)
            op_hor = ((-1, -1), -1)
            op_ver = ((-1, -1), -1)
            op_sow = ((-1, -1), -1)
            op_now = ((-1, -1), -1)

            hor = hwin_blk(5, (x, y), 0, player, node_board)            # Look for player's winning blocks
            ver = vwin_blk(5, (x, y), 0, player, node_board)
            sow = swwin_blk(5, (x, y), 0, player, node_board)
            now = nwwin_blk(5, (x, y), 0, player, node_board)

            op_hor = hwin_blk(5, (x, y), 0, opponent, node_board)       # Look for opponent's winning blocks
            op_ver = vwin_blk(5, (x, y), 0, opponent, node_board)
            op_sow = swwin_blk(5, (x, y), 0, opponent, node_board)
            op_now = nwwin_blk(5, (x, y), 0, opponent, node_board)

            if hor[1] > 0:                                              # Counts number of pieces
                value += pow(base, hor[1])
            if ver[1] > 0:
                value += pow(base, ver[1])
            if sow[1] > 0:
                value += pow(base, sow[1])
            if now[1] > 0:
                value += pow(base, now[1])

            if op_hor[1] > 0:                                           # Counts opponent's pieces
                value -= pow(base, op_hor[1])
            if op_ver[1] > 0:
                value -= pow(base, op_ver[1])
            if op_sow[1] > 0:
                value -= pow(base, op_sow[1])
            if op_now[1] > 0:
                value -= pow(base, op_now[1])

    return value

# Finds winning blocks for reflex agent
# player  - number of the player (see above)
# (x, y)  - starting space of winning blocks
# current - current best winning block
# Returns most left and down blank space in winning block with most pieces and number of pieces in the block
def find_win_blks(player, (x, y), current):
    new = current

    if board[x][y] == player or board[x][y] == 0:                       # Look for horiznotal winning block. Replace new if more left or down
        win_blk = hwin_blk(5, (x, y), 0, player)
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

        win_blk = vwin_blk(5, (x, y), 0, player)
        if win_blk != ((-1, -1), -1):                                   # Vertical
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

        win_blk = nwwin_blk(5, (x, y), 0, player)                       # Diagonal
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

        win_blk = swwin_blk(5, (x, y), 0, player)                       # Other Diagonal
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

    return new

# Recursive helper function
# Find a horizontal winning block
# length     - for recursive call
# (x, y)     - current spot
# n          - number of pieces in block
# player     - number of the player (see above)
# node_board - default current board state
#            - for minimax and alpha beta, replace with potential board state
# Returns last spot in winning block and number of pieces in winning block
def hwin_blk(length, (x, y), n, player, node_board=board):
    if length == 1:
        if node_board[x][y] == player:
            return ((x, y), n + 1)
        if node_board[x][y] == 0:
            return ((x, y), n)

    if x == 6:
        return ((-1, -1), -1)
    if node_board[x][y] == player:
        return hwin_blk(length - 1, (x + 1, y), n + 1, player, node_board)
    if node_board[x][y] == 0:
        return hwin_blk(length - 1, (x + 1, y), n, player, node_board)
        
    return ((-1, -1), -1)           # No winning block found

# See above
def vwin_blk(length, (x, y), n, player, node_board=board):
    if length == 1:
        if node_board[x][y] == player:
            return ((x, y), n + 1)
        if node_board[x][y] == 0:
            return ((x, y), n)

    if y == 6:
        return ((-1, -1), -1)
    if node_board[x][y] == player:
        return vwin_blk(length - 1, (x, y + 1), n + 1, player, node_board)
    if node_board[x][y] == 0:
        return vwin_blk(length - 1, (x, y + 1), n, player, node_board)
        
    return ((-1, -1), -1)

# See above
def nwwin_blk(length, (x, y), n, player, node_board=board):
    if length == 1:
        if node_board[x][y] == player:
            return ((x, y), n + 1)
        if node_board[x][y] == 0:
            return ((x, y), n)

    if x == 6 or y == 0:
        return ((-1, -1), -1)
    if node_board[x][y] == player:
        return nwwin_blk(length - 1, (x + 1, y - 1), n + 1, player, node_board)
    if node_board[x][y] == 0:
        return nwwin_blk(length - 1, (x + 1, y - 1), n, player, node_board)
        
    return ((-1, -1), -1)

# See above
def swwin_blk(length, (x, y), n, player, node_board=board):
    if length == 1:
        if node_board[x][y] == player:
            return ((x, y), n + 1)
        if node_board[x][y] == 0:
            return ((x, y), n)

    if x == 6 or y == 6:
        return ((-1, -1), -1)
    if node_board[x][y] == player:
        return swwin_blk(length - 1, (x + 1, y + 1), n + 1, player, node_board)
    if node_board[x][y] == 0:
        return swwin_blk(length - 1, (x + 1, y + 1), n, player, node_board)
        
    return ((-1, -1), -1)

# Recursively finds the most left and down blank spot in a winning block
# curr - current spot
# end  - end of block
def find_blank(curr, end):
    if curr == end:
        return curr

    if board[curr[0]][curr[1]] == 0:
        return curr

    new = curr
    if end[0] > curr[0]:
        new = (curr[0] + 1, new[1])
    if end[1] > curr[1]:
        new = (new[0], curr[1] + 1)
    if end[1] < curr[1]:
        new = (new[0], curr[1] - 1)

    return find_blank(new, end)

# Plays two agents aginst each other
# type: 1 = reflex
#       2 = minimax
#       3 = alpha beta
def play(red_type, blue_type):
    first = True    # Flag for reflex agent first move

    while True:
        red_win = 1         # 1 = no win yet
        blue_win = 1        # 0 = win

        if red_type == 1:
            red_win = reflex_place_piece(1, first)
        elif red_type == 2:
            red_win = minimax_place_piece(1)
        elif red_type == 3:
            red_win = alpha_beta_place_piece(1)

        if red_win == -1:
            print_board()
            print("Nodes expanded: " + str(nodes_expanded))
            print("No move available to red agent")
            return

        if red_win == 0:
            print_board()
            print("Nodes expanded: " + str(nodes_expanded))
            print("Red wins!")
            return

        if blue_type == 1:
            blue_win = reflex_place_piece(2, first)
        elif blue_type == 2:
            blue_win = minimax_place_piece(2)
        elif blue_type == 3:
            blue_win = alpha_beta_place_piece(2)
        
        if blue_win == -1:
            print_board()
            print("Nodes expanded: " + str(nodes_expanded))
            print("No move available to blue agent")
            return

        if blue_win == 0:
            print_board()
            print("Nodes expanded: " + str(nodes_expanded))
            print("Blue Wins!")
            return

        if first:
            first = False

# Reset nodes_expanded
# Fills entire board with i (for testing)
# i = 0 to reset board
def reset(i):
    global nodes_expanded
    nodes_expanded = 0
    for x in range(7):
        for y in range(7):
            board[x][y] = i

# Places piece according to reflex rules
# player - see above
# first  - flag for first move
def reflex_place_piece(player, first):
    opponent = 0
    if player == 1:
        opponent = 2
    else:
        opponent = 1

    fiar = (7, 7)               # four in a row
    op_fiar = (7, 7)            # opponent four in a row
    op_tiar = (7, 7)            # opponent three in a row
    win_blk = ((7, 7), 0)       # best win block
    for x in range(7):          # Finds best fiar, op_fiar, op_tiar, and win_blk. Best as defined in problem
        for y in range(7):
            fiar = find_chains(player, 4, (x, y), fiar, False)
            op_fiar = find_chains(opponent, 4, (x, y), op_fiar, False)
            op_tiar = find_chains(opponent, 3, (x, y), op_tiar, False)
            win_blk = find_win_blks(player, (x, y), win_blk)
    
    if first:                           # If first move, place randomly
            x = random.randint(0, 6)
            y = random.randint(0, 6)
            if board[x][y] == 0:
                board[x][y] = player
                return 1

    if fiar != (7, 7):                                  # If fiar was found, place piece
        board[fiar[0]][fiar[1]] = player
        return 0
    elif op_fiar != (7, 7):                             # If op_fiar was found, place piece
        board[op_fiar[0]][op_fiar[1]] = player
        return 1
    elif op_tiar != (7, 7):                             # if op_tiar was found, place piece
        board[op_tiar[0]][op_tiar[1]] = player
        return 1
    elif win_blk != ((7, 7), 0):                        # If winning block was found, place piece
        board[win_blk[0][0]][win_blk[0][1]] = player
        if win_blk[1] == 4:                             # If winning block had four piece, then agent won
            return 0
        else:
            return 1

    return -1                                           # Agent has no winning moves left

# Finds the best chain of given length as defined by problem (most left most down)
# length  - length of desired chain
# (x, y)  - spot we are searching from
# current - current best chain
# five    - flag for five or more in a row
# returns best blank spot
# if not blank spot, returns (7, 7)
def find_chains(player, length, (x, y), current, five):
    new = current

    if board[x][y] == player:                                   # checks if player has piece at (x, y). otherwise don't bother looking
        chain = hchain(length, (x, y), player, five)            # Horizontal chain
        if chain != (-1, -1):
            if five and chain < new:                            # Five, don't bother looking for blank spots
                return chain
            if x > 0 and board[x - 1][y] == 0 and (x - 1, y) < new:     # New best is blank spot at beginning of chian
                new = (x - 1, y)
            elif chain[0] < 6 and board[chain[0] + 1][y] == 0 and (chain[0] + 1, y) < new:      # New best is blank spot at end of chain
                new = (chain[0] + 1, y)

        chain = vchain(length, (x, y), player, five)            # Vertical 
        if chain != (-1, -1):
            if five and chain < new:
                return chain
            if y > 0 and board[x][y - 1] == 0 and (x, y - 1) < new:
                new = (x, y - 1)
            elif chain[1] < 6 and board[x][chain[1] + 1] == 0 and (x, chain[1] + 1) < new:
                new = (x, chain[1] + 1)
                
        chain = nwchain(length, (x, y), player, five)           # Diagonal
        if chain != (-1, -1):
            if five and chain < new:
                return chain
            if x > 0 and y < 6 and board[x - 1][y + 1] == 0 and (x - 1, y + 1) < new:
                new = (x - 1, y + 1)
            elif chain[0] < 6 and chain[1] > 0 and board[chain[0] + 1][chain[1] - 1] == 0 and (chain[0] + 1, chain[1] - 1) < new:
                new = (chain[0] + 1, chain[1] - 1)

        chain = swchain(length, (x, y), player, five)           # Other diagonal
        if chain != (-1, -1):
            if five and chain < new:
                return chain
            if x > 0 and y > 0 and board[x - 1][y - 1] == 0 and (x - 1, y - 1) < new:
                new = (x - 1, y - 1)
            elif chain[0] < 6 and chain[1] < 6 and board[chain[0] + 1][chain[1] + 1] == 0 and (chain[0] + 1, chain[1] + 1) < new:
                new = (chain[0] + 1, chain[1] + 1)

    return new

# Helper function for finding chains
# Recursively finds a horizontal chain
# length - for recursive call
# (x, y) - current spot
# player - you should know by now
# five   - same as above
def hchain(length, (x, y), player, five):
    if length == 0 and board[x][y] != player:
        return (x - 1, y)
    elif length == 0 and five:
        return (x - 1, y)

    if x == 6:
        return (-1, -1)
    if board[x][y] == player:
        return hchain(length - 1, (x + 1, y), player, five)
    else:
        return (-1, -1)

# i'm not gonna even write see above anymore
def vchain(length, (x, y), player, five):
    if length == 0 and board[x][y] != player:
        return (x, y - 1)
    elif length == 0 and five:
        return (x, y - 1)

    if y == 6:
        return (-1, -1)
    if board[x][y] == player:
        return vchain(length - 1, (x, y + 1), player, five)
    else:
        return (-1, -1)

def nwchain(length, (x, y), player, five):
    if length == 0 and board[x][y] != player:
        return (x - 1, y + 1)
    elif length == 0 and five:
        return (x - 1, y + 1)

    if x == 6 or y == 0:
        return (-1, -1)
    if board[x][y] == player:
        return nwchain(length - 1, (x + 1, y - 1), player, five)
    else:
        return (-1, -1)

def swchain(length, (x, y), player, five):
    if length == 0 and board[x][y] != player:
        return (x - 1, y - 1)
    elif length == 0 and five:
        return (x - 1, y - 1)

    if x == 6 or y == 6:
        return (-1, -1)
    if board[x][y] == player:
        return swchain(length - 1, (x + 1, y + 1), player, five)
    else:
        return (-1, -1)

# Prints the board because numpy array stores it in wrong orientation
def print_board(b=board):
    for y in reversed(range(7)):
        temp = []
        for x in range(7):
            temp.append(b[x][y])
        print(np.array(temp))
