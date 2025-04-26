from my_chess.pieces import piece_validate
from my_chess.pieces import can_piece_be_captured
def process_move(move, myGame):
    move = prase_move(move)
    if validate_move(move, myGame) != True:
        print(validate_move(move, myGame))
        return
    capturing_pieces = "upper" if myGame.turn == "black" else "lower"
    make_move(move, myGame)
    if capturing_pieces == "upper":
        coordinate = myGame.black_king_coordinates
    else:
        coordinate = myGame.white_king_coordinates
    if can_piece_be_captured(coordinate,myGame,capturing_pieces) == True:
        print(myGame.board.board)
        print("Cannot move to that position, it puts you in check")
        undo_move(myGame)
def process_move_ai(move, myGame):
    make_move(move, myGame)
def prase_move(move):
    inital = move[:2]
    final = move[2:]
    inital = (8 - int(inital[1]) + 2, ord(inital[0]) - ord("a") + 2)
    final = (8 - int(final[1]) + 2, ord(final[0]) - ord("a") + 2)
    #print(inital, final)
    return (inital, final)
def validate_move(move, myGame):
    myBoard = myGame.board
    turn = myGame.turn
    #check if move is on the myBoard
    if move[0][0] < 2 or move[0][0] > 9 or move[0][1] < 2 or move[0][1] > 9 or move[1][0] < 2 or move[1][0] > 9 or move[1][1] < 2 or move[1][1] > 9:
        return "Move is off the board"
    #check if there is a piece
    piece = str(myBoard.get_piece(move[0]))
    if piece == "0":
        return "No piece at that position"
    #check if piece belongs to player
    if piece.islower() and turn == "white":
        return "Piece does not belong to player"
    if piece.isupper() and turn == "black":
        return "Piece does not belong to player"
    if not piece_validate(piece, move, myGame, False):
        return "Piece cannot move to that position"
    return True
def validate_move_verifying(move, myGame):
    myBoard = myGame.board
    turn = myGame.turn
    #check if move is on the myBoard
    if move[0][0] < 2 or move[0][0] > 9 or move[0][1] < 2 or move[0][1] > 9 or move[1][0] < 2 or move[1][0] > 9 or move[1][1] < 2 or move[1][1] > 9:
        return "Move is off the board"
    #check if there is a piece
    piece = str(myBoard.get_piece(move[0]))
    if piece == "0":
        return "No piece at that position"
    #check if piece belongs to player
    if piece.islower() and turn == "white":
        return "Piece does not belong to player"
    if piece.isupper() and turn == "black":
        return "Piece does not belong to player"
    if not piece_validate(piece, move, myGame, True):
        return "Piece cannot move to that position"
    return True
def make_move(move, myGame):
    update_stack(myGame)
    inital = move[0]
    final = move[1]
    #print("Moving {piece} from {inital} to {final}".format(piece=myGame.board.get_piece(move[0]), inital=inital, final=final))
    myBoard = myGame.board
    piece = myGame.board.get_piece(move[0])
    captured_piece = myGame.board.get_piece(move[1])
    #update if en passant is valid
    if inital[1] == final[1] and abs(inital[0]-final[0]) == 2:
        if piece == "P":
            myGame.white_valid_en_passant = (True, final[1])
        if piece == "p":
            myGame.black_valid_en_passant = (True, final[1])
    #for en passant - white
    if inital[0] == 5 and final[0] == 4 and abs(inital[1] - final[1]) == 1 and piece == "P":
        if myBoard.get_piece((inital[0], final[1])) == "p" and myGame.black_valid_en_passant == (True,final[1]):
            myBoard.board[inital[0]][final[1]] = "0"
            myGame.board.board[move[0][0]][move[0][1]] = "0"
            myGame.board.board[move[1][0]][move[1][1]] = piece
            myGame.turn_num += 1
            if myGame.turn == "white":
                myGame.black_valid_en_passant = (False, -1)
            else:
                myGame.white_valid_en_passant = (False, -1)
            myGame.previous_turn = (inital,final,captured_piece)
            myGame.turn = "black" if myGame.turn == "white" else "white"
            return
    #for en passant - black
    if inital[0] == 6 and final[0] == 7 and abs(inital[1] - final[1]) == 1 and piece == "p":
        if myBoard.get_piece((inital[0], final[1])) == "P" and myGame.white_valid_en_passant == (True,final[1]):
            myBoard.board[inital[0]][final[1]] = "0"
            myGame.board.board[move[0][0]][move[0][1]] = "0"
            myGame.board.board[move[1][0]][move[1][1]] = piece
            myGame.turn_num += 1
            if myGame.turn == "white":
                myGame.black_valid_en_passant = (False, -1)
            else:
                myGame.white_valid_en_passant = (False, -1)
            myGame.previous_turn = (inital,final,captured_piece)
            myGame.turn = "black" if myGame.turn == "white" else "white"
            return
    #for pawn replacement
    if final[0] == 2 and piece == "P":
        loop = True
        while loop:
            pawn_replacement = input("Enter the piece you want to promote to (Q, R, B, N): ")
            if pawn_replacement not in ["Q", "R", "B", "N"]:
                print("Invalid piece")
                continue
            myBoard.board[9][final[1]] = pawn_replacement
            myBoard.board[inital[0]][inital[1]] = "0"  
            loop = False
        myGame.turn_num += 1
        if myGame.turn == "white":
            myGame.black_valid_en_passant = (False, -1)
        else:
            myGame.white_valid_en_passant = (False, -1)
        myGame.previous_turn = (inital,final,captured_piece)
        myGame.turn = "black" if myGame.turn == "white" else "white"
        return
    if final[0] == 9 and piece == "p":
        if myGame.mode == "AI":
            print("AI pawn promotion")
            myBoard.board[2][final[1]] = "Q"
            myBoard.board[inital[0]][inital[1]] = "0"
        else:
            loop = True
            while loop:
                pawn_replacement = input("Enter the piece you want to promote to (q, r, b, n): ")
                if pawn_replacement not in ["q", "r", "b", "n"]:
                    print("Invalid piece")
                    continue
                myBoard.board[2][final[1]] = pawn_replacement
                myBoard.board[inital[0]][inital[1]] = "0"  
                loop = False
        myGame.turn_num += 1
        if myGame.turn == "white":
            myGame.black_valid_en_passant = (False, -1)
        else:
            myGame.white_valid_en_passant = (False, -1)
        myGame.previous_turn = (inital,final,captured_piece)
        myGame.turn = "black" if myGame.turn == "white" else "white"
        return
    #For king moves
    if myGame.turn == "white":
        if piece == "K":
            if inital[0] == 9 and inital[1] == 6:
                if final[0] == 9 and final[1] == 4:
                    myGame.upper_left_rook_moved = myGame.turn_num
                    myBoard.board[9][2] = "0"
                    myBoard.board[9][5] = "R"
                if final[0] == 9 and final[1] == 8:
                    myGame.upper_right_rook_moved = myGame.turn_num
                    myBoard.board[9][9] = "0"
                    myBoard.board[9][7] = "R"
            #update king status if being moved
            myGame.white_valid_castling = False
            #print("White king moved")
            #print("White king coordinates: {final}".format(final=final))
            myGame.white_king_coordinates = final
        if piece == "R":
            if inital[0] == 9 and inital[1] == 2 and myGame.upper_left_rook_moved == -1:
                myGame.upper_left_rook_moved = myGame.turn_num
            if inital[0] == 9 and inital[1] == 9 and myGame.upper_right_rook_moved == -1:
                myGame.upper_right_rook_moved = myGame.turn_num
    if myGame.turn == "black":
        if piece == "k":
            if inital[0] == 2 and inital[1] == 6:
                if final[0] == 2 and final[1] == 4:
                    myGame.lower_left_rook_moved = myGame.turn_num
                    myBoard.board[2][2] = "0"
                    myBoard.board[2][5] = "r"
                if final[0] == 2 and final[1] == 8:
                    myGame.lower_right_rook_moved = myGame.turn_num
                    myBoard.board[2][9] = "0"
                    myBoard.board[2][7] = "r"
            #update king status if being moved
            myGame.black_valid_castling = False
            myGame.black_king_coordinates = final
            #update rook status if being moved
        if piece == "r":
            if inital[0] == 2 and inital[1] == 2 and myGame.lower_left_rook_moved == -1:
                myGame.lower_left_rook_moved = myGame.turn_num
            if inital[0] == 2 and inital[1] == 9 and myGame.lower_right_rook_moved == -1:
                myGame.lower_right_rook_moved = myGame.turn_num
    #print("Moving {piece} from {move[0]} to {move[1]}".format(piece=piece, move=move))
    myGame.board.board[move[0][0]][move[0][1]] = "0"
    myGame.board.board[move[1][0]][move[1][1]] = piece
    myGame.turn_num += 1
    if myGame.turn == "white":
        myGame.black_valid_en_passant = (False, -1)
    else:
        myGame.white_valid_en_passant = (False, -1)
    myGame.previous_turn = (inital,final,captured_piece)
    myGame.turn = "black" if myGame.turn == "white" else "white"
#def is_check(myGame,turn):
#    if turn == "white":
#        king_coordinates = myGame.white_king_coordinates
#    else:
#        king_coordinates = myGame.black_king_coordinates
#    if can_piece_be_captured(king_coordinates, myGame) == True:
#        return True
#    return False
def undo_move(myGame):
    myBoard = myGame.board
    previous_turn_inital = myGame.previous_turn[0]
    previous_turn_final = myGame.previous_turn[1]
    captured_piece = myGame.previous_turn[2]
    moved_piece = myGame.board.get_piece(previous_turn_final)
    #if castling
    if abs(previous_turn_inital[1] - previous_turn_final[1]) == 2:
        if moved_piece == "K":
            if previous_turn_final[1] == 4:
                myBoard.board[9][2] = "R"
                myBoard.board[9][5] = "0"
            if previous_turn_final[1] == 8:
                myBoard.board[9][9] = "R"
                myBoard.board[9][7] = "0"
        if moved_piece == "k":
            if previous_turn_final[1] == 4:
                myBoard.board[2][2] = "r"
                myBoard.board[2][5] = "0"
            if previous_turn_final[1] == 8:
                myBoard.board[2][9] = "r"
                myBoard.board[2][7] = "0"
    #if en passant
    if moved_piece == "P" or moved_piece == "p":
        if abs(previous_turn_inital[1] - previous_turn_final[1]) == 1: 
            if captured_piece == "0":
                column = previous_turn_final[1]
                row = previous_turn_inital[0]
                if moved_piece == "P":
                    myBoard.board[row][column] = "p"
                if moved_piece == "p":
                    myBoard.board[row][column] = "P"
    #if normal move
    myBoard.board[previous_turn_final[0]][previous_turn_final[1]] = captured_piece
    myBoard.board[previous_turn_inital[0]][previous_turn_inital[1]] = moved_piece
    #update board state with stack
    previous_state = myGame.game_stack.pop()
    myGame.turn_num = previous_state['turn_num']
    myGame.previous_turn = previous_state['previous_turn']
    myGame.turn = previous_state['turn']
    myGame.white_valid_castling = previous_state['white_valid_castling']
    myGame.black_valid_castling = previous_state['black_valid_castling']
    myGame.white_king_coordinates = previous_state['white_king_coordinates']
    myGame.black_king_coordinates = previous_state['black_king_coordinates']
    myGame.upper_left_rook_moved = previous_state['upper_left_rook_moved']
    myGame.upper_right_rook_moved = previous_state['upper_right_rook_moved']
    myGame.lower_left_rook_moved = previous_state['lower_left_rook_moved']
    myGame.lower_right_rook_moved = previous_state['lower_right_rook_moved']
    myGame.white_valid_en_passant = previous_state['white_valid_en_passant']
    myGame.black_valid_en_passant = previous_state['black_valid_en_passant']
def is_checkmate_stalemate(myGame,turn):
    myboard = myGame.board
    if turn == "white":
        king_coordinates = myGame.white_king_coordinates
        capturing_pieces = "lower"
    else:  
        king_coordinates = myGame.black_king_coordinates
        capturing_pieces = "upper"
    
    incheck = can_piece_be_captured(king_coordinates, myGame, capturing_pieces)
    #check if king can move to any of the 8 squares around it
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_coordinates = (king_coordinates[0] + i, king_coordinates[1] + j)
            if new_coordinates[0] < 2 or new_coordinates[0] > 9 or new_coordinates[1] < 2 or new_coordinates[1] > 9:
                continue
            if myboard.get_piece(new_coordinates) == "0" or (myboard.get_piece(new_coordinates).islower() and turn == "white") or (myboard.get_piece(new_coordinates).isupper() and turn == "black"):
                #create test game to new move
                make_move((king_coordinates, new_coordinates), myGame)
                if can_piece_be_captured(new_coordinates, myGame,capturing_pieces) == False:
                    #print("King can move out of check")
                    #print("King can move to {new_coordinates}".format(new_coordinates=new_coordinates))
                    undo_move(myGame)
                    if incheck == True:
                        return 3
                    return 0
                undo_move(myGame)
    #check if any piece can block the attack
    for i in range(2, 10):
        for j in range(2, 10):
            piece = myboard.get_piece((i, j))
            #print("Piece at {i},{j}: {piece}".format(i=i, j=j, piece=piece))
            if piece == "0":
                continue
            if (piece.islower() or piece == "K") and turn == "white":
                continue
            if (piece.isupper() or piece == "k") and turn == "black":
                continue
            #test all possible moves for other pieces
            for g in range(2, 10):
                for h in range(2,10):
                    if validate_move(((i,j),(g,h)), myGame) == True:
                        #make move
                        make_move(((i,j),(g,h)), myGame)
                        if can_piece_be_captured(king_coordinates,myGame, capturing_pieces) == False:
                            undo_move(myGame)
                            if incheck == True:
                                return 3
                            return 0
                        #reset test game
                        undo_move(myGame)
                        
    #print("No pieces can block the attack")
    if incheck == True:
        return 1
    else:
        return 2

def update_stack(myGame):
    board_state = {
        'turn_num': myGame.turn_num,
        'previous_turn': myGame.previous_turn,
        'turn': myGame.turn,
        'white_valid_castling': myGame.white_valid_castling,
        'black_valid_castling': myGame.black_valid_castling,
        'white_king_coordinates': myGame.white_king_coordinates,
        'black_king_coordinates': myGame.black_king_coordinates,
        'upper_left_rook_moved': myGame.upper_left_rook_moved,
        'upper_right_rook_moved': myGame.upper_right_rook_moved,
        'lower_left_rook_moved': myGame.lower_left_rook_moved,
        'lower_right_rook_moved': myGame.lower_right_rook_moved,
        'white_valid_en_passant': myGame.white_valid_en_passant,
        'black_valid_en_passant': myGame.black_valid_en_passant,
    }
    myGame.game_stack.append(board_state)