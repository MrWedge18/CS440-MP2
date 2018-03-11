import numpy as np
import random
from math import pow

board = np.zeros((7, 7))        # 0 = empty, 1 = red, 2 = blue
base = 5

class Node:
    def __init__(self, parent, board, player, piece):
        self.parent = parent
        self.board = np.copy(board)
        self.board[piece[0]][piece[1]] = player

def minimax_place_piece(player):

# reCURSE
minimax(node, depth, player):
    if depth == 3:
        return eva(node.board, player)

    max = asdf
    min = -1

    for x in range(7):
        for y in range (7):

    

def eva(board, player):
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

            if x > 0:
                if board[x - 1][y] != player:
                    hor = hwin_blk(5, (x, y), 0, player)
                if board[x - 1][y] != opponent:
                    op_hor = hwin_blk(5, (x, y), 0, opponent)
            if y > 0:
                if board[x][y - 1] != player:
                    ver = vwin_blk(5, (x, y), 0, player)
                if board[x][y - 1] != opponent:
                    op_ver = vwin_blk(5, (x, y), 0, opponent)
            if x > 0 and y > 0:
                if board[x - 1][y - 1] != player:
                    sow = swwin_blk(5, (x, y), 0, player)
                if board[x - 1][y - 1] != opponent:
                    op_sow = swwin_blk(5, (x, y), 0, opponent)
            if x > 0 and y < 6:
                if board[x - 1][y + 1] != player:
                    now = nwwin_blk(5, (x, y), 0, player)
                if board[x - 1][y + 1] != opponent:
                    op_now = nwwin_blk(5, (x, y), 0, opponent)


            if hor[1] != -1:
                value += pow(base, hor[1])
            if ver[1] != -1:
                value += pow(base, ver[1])
            if sow[1] != -1:
                value += pow(base, sow[1])
            if now[1] != -1:
                value += pow(base, now[1])

            if op_hor[1] != -1:
                value -= pow(base, op_hor[1])
            if op_ver[1] != -1:
                value -= pow(base, op_ver[1])
            if op_sow[1] != -1:
                value -= pow(base, op_sow[1])
            if op_now[1] != -1:
                value -= pow(base, op_now[1])

            return value

def find_win_blks(player, (x, y), current):
    new = current

    if board[x][y] == player or board[x][y] == 0:
        win_blk = hwin_blk(5, (x, y), 0, player)
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

        win_blk = vwin_blk(5, (x, y), 0, player)
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

        win_blk = nwwin_blk(5, (x, y), 0, player)
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

        win_blk = swwin_blk(5, (x, y), 0, player)
        if win_blk != ((-1, -1), -1):
            if win_blk[1] > new[1]:
                new = (find_blank((x, y), win_blk[0]), win_blk[1])
            elif win_blk[1] == new[1]:
                blank = find_blank((x, y), win_blk[0])
                if blank < new[0]:
                    new = (blank, new[1])

    return new

def hwin_blk(length, (x, y), n, player):
    if length == 1:
        if board[x][y] == player:
            return ((x, y), n + 1)
        if board[x][y] == 0:
            return ((x, y), n)

    if x == 6:
        return ((-1, -1), -1)
    if board[x][y] == player:
        return hwin_blk(length - 1, (x + 1, y), n + 1, player)
    if board[x][y] == 0:
        return hwin_blk(length - 1, (x + 1, y), n, player)
        
    return ((-1, -1), -1)

def vwin_blk(length, (x, y), n, player):
    if length == 1:
        if board[x][y] == player:
            return ((x, y), n + 1)
        if board[x][y] == 0:
            return ((x, y), n)

    if y == 6:
        return ((-1, -1), -1)
    if board[x][y] == player:
        return vwin_blk(length - 1, (x, y + 1), n + 1, player)
    if board[x][y] == 0:
        return vwin_blk(length - 1, (x, y + 1), n, player)
        
    return ((-1, -1), -1)

def nwwin_blk(length, (x, y), n, player):
    if length == 1:
        if board[x][y] == player:
            return ((x, y), n + 1)
        if board[x][y] == 0:
            return ((x, y), n)

    if x == 6 or y == 0:
        return ((-1, -1), -1)
    if board[x][y] == player:
        return nwwin_blk(length - 1, (x + 1, y - 1), n + 1, player)
    if board[x][y] == 0:
        return nwwin_blk(length - 1, (x + 1, y - 1), n, player)
        
    return ((-1, -1), -1)

def swwin_blk(length, (x, y), n, player):
    if length == 1:
        if board[x][y] == player:
            return ((x, y), n + 1)
        if board[x][y] == 0:
            return ((x, y), n)

    if x == 6 or y == 6:
        return ((-1, -1), -1)
    if board[x][y] == player:
        return swwin_blk(length - 1, (x + 1, y + 1), n + 1, player)
    if board[x][y] == 0:
        return swwin_blk(length - 1, (x + 1, y + 1), n, player)
        
    return ((-1, -1), -1)

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

# type: 1 = reflex
#       2 = minimax
#       3 = alpha beta
def play(red_type, blue_type):
    first = True
    while True:
        red_win = 1
        blue_win = 1
        if red_type == 1:
            red_win = reflex_place_piece(1, first)
#       elif red_type == 2:
#           red_win = minimax_place_piece(1)
#       elif red_type == 3:
#           red_win = alpha_beta_place_piece(1)

        if red_win == -1:
            print("No move available to red agent")
            print_board()
            return

        if red_win == 0:
            print("Red wins!")
            print_board()
            return

        if blue_type == 1:
            blue_win = reflex_place_piece(2, first)
        
        if blue_win == -1:
            print("No move available to blue agent")
            print_board()
            return

        if blue_win == 0:
            print("Blue Wins!")
            print_board()
            return

        if first:
            first = False

def reset():
    for x in range(7):
        for y in range(7):
            board[x][y] = 0

def reflex_place_piece(player, first):
    opponent = 0
    if player == 1:
        opponent = 2
    else:
        opponent = 1

    fiar = (7, 7)
    op_fiar = (7, 7)
    op_tiar = (7, 7)
    win_blk = ((7, 7), 0)
    for x in range(7):
        for y in range(7):
            fiar = find_chains(player, 4, (x, y), fiar)
            op_fiar = find_chains(opponent, 4, (x, y), op_fiar)
            op_tiar = find_chains(opponent, 3, (x, y), op_tiar)
            win_blk = find_win_blks(player, (x, y), win_blk)
    
    if fiar != (7, 7):
        board[fiar[0]][fiar[1]] = player
        return 0
    elif op_fiar != (7, 7):
        board[op_fiar[0]][op_fiar[1]] = player
        return 1
    elif op_tiar != (7, 7):
        board[op_tiar[0]][op_tiar[1]] = player
        return 1
    elif win_blk != ((7, 7), 0):
        board[win_blk[0][0]][win_blk[0][1]] = player
        if win_blk[1] == 4:
            return 0
        else:
            return 1
    elif first:
            x = random.randint(0, 6)
            y = random.randint(0, 6)
            if board[x][y] == 0:
                board[x][y] = player
                return 1


    return -1   # board is full

def find_chains(player, length, (x, y), current):
    new = current

    if board[x][y] == player:
        chain = hchain(length, (x, y), player)
        if chain != (-1, -1):
            if x > 0 and board[x - 1][y] == 0 and (x - 1, y) < new:
                new = (x - 1, y)
            elif chain[0] < 6 and board[chain[0] + 1][y] == 0 and (chain[0] + 1, y) < new:
                new = (chain[0] + 1, y)

        chain = vchain(length, (x, y), player)
        if chain != (-1, -1):
            if y > 0 and board[x][y - 1] == 0 and (x, y - 1) < new:
                new = (x, y - 1)
            elif chain[1] < 6 and board[x][chain[1] + 1] == 0 and (x, chain[1] + 1) < new:
                new = (x, chain[1] + 1)
                
        chain = nwchain(length, (x, y), player)
        if chain != (-1, -1):
            if x > 0 and y < 6 and board[x - 1][y + 1] == 0 and (x - 1, y + 1) < new:
                new = (x - 1, y + 1)
            elif chain[0] < 6 and chain[1] > 0 and board[chain[0] + 1][chain[1] - 1] == 0 and (chain[0] + 1, chain[1] - 1) < new:
                new = (chain[0] + 1, chain[1] - 1)

        chain = swchain(length, (x, y), player)
        if chain != (-1, -1):
            if x > 0 and y > 0 and board[x - 1][y - 1] == 0 and (x - 1, y - 1) < new:
                new = (x - 1, y - 1)
            elif chain[0] < 6 and chain[1] < 6 and board[chain[0] + 1][chain[1] + 1] == 0 and (chain[0] + 1, chain[1] + 1) < new:
                new = (chain[0] + 1, chain[1] + 1)

    return new

def hchain(length, (x, y), player):
    if length == 0 and board[x][y] != player:
        return (x - 1, y)

    if x == 6:
        return (-1, -1)
    if board[x][y] == player:
        return hchain(length - 1, (x + 1, y), player)
    else:
        return (-1, -1)

def vchain(length, (x, y), player):
    if length == 0 and board[x][y] != player:
        return (x, y - 1)

    if y == 6:
        return (-1, -1)
    if board[x][y] == player:
        return vchain(length - 1, (x, y + 1), player)
    else:
        return (-1, -1)

def nwchain(length, (x, y), player):
    if length == 0 and board[x][y] != player:
        return (x - 1, y + 1)
    if x == 6 or y == 0:
        return (-1, -1)
    if board[x][y] == player:
        return nwchain(length - 1, (x + 1, y - 1), player)
    else:
        return (-1, -1)

def swchain(length, (x, y), player):
    if length == 0 and board[x][y] != player:
        return (x - 1, y - 1)
    if x == 6 or y == 6:
        return (-1, -1)
    if board[x][y] == player:
        return swchain(length - 1, (x + 1, y + 1), player)
    else:
        return (-1, -1)


def print_board():
    for y in reversed(range(7)):
        temp = []
        for x in range(7):
            temp.append(board[x][y])
        print(np.array(temp))
