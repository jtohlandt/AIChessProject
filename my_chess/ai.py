import multiprocessing
import copy
from my_chess.move import *

def ai_move(myGame):
    minimax_depth = 4
    alpha = float('-inf')
    beta = float('inf')
    #score, bestMove = minimax(myGame, minimax_depth, True, alpha, beta)
    #score, bestMove = minimax_no_pruning(myGame, minimax_depth, True)
    first_round_moves = generate_legal_moves(myGame)
    #generate pool of workers
    with multiprocessing.Pool() as pool:
        arguments = [(copy.deepcopy(myGame), move, minimax_depth-1, False, alpha, beta) for move in first_round_moves]
        results = pool.starmap(minimax_wrapper, arguments)

    #pick the best move from workers
    best_score = float('-inf')
    bestMove = None
    for score, move in results:
        if score > best_score:
            best_score = score
            bestMove = move
    return bestMove

def minimax_wrapper(myGame, move, depth, maximizingPlayer, alpha, beta):
    make_move(move, myGame)
    score, _ = minimax(myGame, depth, maximizingPlayer, alpha, beta)
    return score, move

def generate_legal_moves(myGame):
    myBoard = myGame.board
    legal_moves = []
    if myGame.turn == "black":
        for row in range(2,10):
            for col in range(2,10):
                piece = myBoard.board[row][col]
                if piece.islower():
                    inital = (row, col)
                    for row2 in range(2,10):
                        for col2 in range(2,10):
                            final = (row2, col2)
                            piece_final = myBoard.get_piece(final)
                            if piece_final.islower():
                                continue
                            move = (inital, final)
                            if validate_move(move,myGame) == True:
                                legal_moves.append(move)
    if myGame.turn == "white":
        for row in range(2,10):
            for col in range(2,10):
                piece = myBoard.board[row][col]
                if piece.isupper():
                    inital = (row, col)
                    for row2 in range(2,10):
                        for col2 in range(2,10):
                            final = (row2, col2)
                            piece_final = myBoard.get_piece(final)
                            if piece_final.isupper():
                                continue
                            move = (inital, final)
                            if validate_move(move,myGame) == True:
                                legal_moves.append(move)
    return (legal_moves)

def score(myGame, penalty = 0):
    myBoard = myGame.board
    score = 0
    piece_value = {'P': -1, 'N': -3, 'B': -3, 'R': -5, 'Q': -9, 'K': 0, 'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}
    for row in range(2, 10):
        for col in range(2, 10):
            piece = myBoard.board[row][col]
            if piece != '0':
                    score += piece_value[piece]
    score += penalty
    return score

def minimax(myGame, depth, maximizingPlayer, alpha, beta):
    best_move = None
    king_status = is_checkmate_stalemate(myGame, myGame.turn)
    if depth == 0 or king_status in (1, 2):
        if king_status == 1: #checkmate
            return (-9999,None) if maximizingPlayer else (9999, None)
        elif king_status == 2: #stalemate
            return (0, None)
        if depth == 0 and king_status == 3:
                penalty = 1 if myGame.turn == "black" else -1
                return score(myGame,penalty), None
        return score(myGame), None
    legal_moves = generate_legal_moves(myGame)
    if maximizingPlayer:
        maxEval = float('-inf')
        for move in legal_moves:
            make_move(move, myGame)
            eval, _ = minimax(myGame, depth - 1, False, alpha, beta)
            undo_move(myGame)
            if eval > maxEval:
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        for move in legal_moves:
            make_move(move, myGame)
            eval, _ = minimax(myGame, depth - 1, True, alpha, beta)
            undo_move(myGame)
            if eval < minEval:
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move
def minimax_no_pruning(myGame, depth, maximizingPlayer):
    best_move = None
    if depth == 0 or is_checkmate_stalemate(myGame, myGame.turn) == 2 or is_checkmate_stalemate(myGame, myGame.turn) == 1:
        return score(myGame), None
    legal_moves = generate_legal_moves(myGame)
    if maximizingPlayer:
        maxEval = float('-inf')
        for move in legal_moves:
            make_move(move, myGame)
            eval, _ = minimax_no_pruning(myGame, depth - 1, False)
            undo_move(myGame)
            if eval > maxEval:
                maxEval = eval
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        for move in legal_moves:
            make_move(move, myGame)
            eval, _ = minimax_no_pruning(myGame, depth - 1, True)
            undo_move(myGame)
            if eval < minEval:
                minEval = eval
                best_move = move
        return minEval, best_move

'''
TESTING
#print("Move: ", move)
#myGame_copy = copy.deepcopy(myGame)

#myGame.board.print_board()
#myGame.board.print_board()

print(move)
print(myGame.previous_turn)
myGame_copy.board.print_board()
myGame.board.print_board()
assert myGame_copy.mode == myGame.mode, "Game mode was not restored correctly"
assert myGame_copy.game_stack == myGame.game_stack, "Game stack was not restored correctly"
assert myGame_copy.turn_num == myGame.turn_num, "Turn number was not restored correctly"
assert myGame_copy.previous_turn == myGame.previous_turn, "Previous turn was not restored correctly"
assert myGame_copy.turn == myGame.turn, "Turn was not restored correctly"
assert myGame_copy.white_valid_castling == myGame.white_valid_castling, "White castling was not restored correctly"
assert myGame_copy.black_valid_castling == myGame.black_valid_castling, "Black castling was not restored correctly"
assert myGame_copy.white_king_coordinates == myGame.white_king_coordinates, "White king coordinates were not restored correctly"
assert myGame_copy.black_king_coordinates == myGame.black_king_coordinates, "Black king coordinates were not restored correctly"
assert myGame_copy.upper_left_rook_moved == myGame.upper_left_rook_moved, "Upper left rook moved was not restored correctly"
assert myGame_copy.upper_right_rook_moved == myGame.upper_right_rook_moved, "Upper right rook moved was not restored correctly"
assert myGame_copy.lower_left_rook_moved == myGame.lower_left_rook_moved, "Lower left rook moved was not restored correctly"
assert myGame_copy.lower_right_rook_moved == myGame.lower_right_rook_moved, "Lower right rook moved was not restored correctly"
assert myGame_copy.white_valid_en_passant == myGame.white_valid_en_passant, "White en passant was not restored correctly"
assert myGame_copy.black_valid_en_passant == myGame.black_valid_en_passant, "Black en passant was not restored correctly"
assert myGame_copy.board.board == myGame.board.board, "Board was not restored correctly"
'''