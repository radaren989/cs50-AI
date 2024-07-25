"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    iEmptyFields = sum(row.count(EMPTY) for row in board)

    return X if (9 - iEmptyFields) % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionList = []

    for i, row in enumerate(board):
        actionList.extend((i, j) for j, value in enumerate(row) if value == EMPTY)

    return actionList

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)

    i, j = action
    if board[i][j] != EMPTY:
        raise IllegalMoveError(f"{action} is an illegal move!")
    
    newBoard = copy.deepcopy(board)
    newBoard[i][j] = turn

    return newBoard

class IllegalMoveError(Exception):
    def __init__(self, message):
        super().__init__(message)

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = utility(board) 
    if  win == 1:
        return X
    elif win == -1:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if utility(board) != 0:
        return True
    
    # Check if the board is full (no empty spaces)
    if sum(row.count(EMPTY) for row in board) == 0:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    for player in [X, O]:
        # Check rows and columns
        for i in range(3):
            if (board[i][0] == board[i][1] == board[i][2] == player or  # Row check
                board[0][i] == board[1][i] == board[2][i] == player):   # Column check
                return 1 if player == X else -1

        # Check diagonals
        if (board[0][0] == board[1][1] == board[2][2] == player or  # Main diagonal check
            board[0][2] == board[1][1] == board[2][0] == player):   # Anti-diagonal check
            return 1 if player == X else -1

    # No winner yet
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    possibleActions = actions(board)
    if player(board) == X:
        max = -5
        move = ()
        for action in possibleActions:
            val = minValue(result(board, action))

            if max < val:
                max = val
                move = action

        return move

    else:
        min = 5
        move = ()
        for action in possibleActions:
            val = maxValue(result(board, action))

            if min > val:
                min = val
                move = action

        return move

def minValue(board):
    if terminal(board):
        return utility(board)
    
    possibleAcrions = actions(board)
    val = 5
    for action in possibleAcrions:
        val = min(val, maxValue(result(board, action)))

    return val

def maxValue(board):
    if terminal(board):
        return utility(board)
    
    possibleAcrions = actions(board)
    val = -5
    for action in possibleAcrions:
        val = max(val, minValue(result(board, action)))
    return val
