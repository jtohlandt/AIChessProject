def piece_validate(piece, move, myGame,verifying):
    myBoard = myGame.board
    if piece == "P":
        return pawn_white_validate(move, myGame,verifying)
    if piece == "p":
        return pawn_black_validate(move, myGame,verifying)
    if piece == "R" or piece == "r":
        return rook_validate(move, myBoard)
    if piece == "N" or piece == "n":
        return knight_validate(move, myBoard)
    if piece == "B" or piece == "b":
        return bishop_validate(move, myBoard)
    if piece == "Q" or piece == "q":
        return queen_validate(move, myBoard, myGame)
    if piece == "K" or piece == "k":
        return king_validate(move, myGame,verifying)
#check if final doesn't have it's own players piece
def verify_own_piece(move, myBoard):
    inital = move[0]
    final = move[1]
    piece = myBoard.get_piece(inital)
    if piece.islower():
        if myBoard.get_piece(final).islower():
            return False
    if piece.isupper():
        if myBoard.get_piece(final).isupper():
            return False

def pawn_white_validate(move, myGame,verifying):
    myBoard = myGame.board
    inital = move[0]
    final = move[1]
    #check if final doesn't have it's own players piece
    if verify_own_piece(move, myBoard) == False:
        return False
    #if move is two spaces forward
    if verifying == False:
        if inital[1] == final[1] and inital[0] - final[0] == 2:
            #check if piece is in valid row
            if inital[0] == 8:
                #check if there is a piece in the way
                if myBoard.get_piece((inital[0] - 1, inital[1])) != "0" or myBoard.get_piece((inital[0] - 2, inital[1])) != "0":
                    return False
                return True
            return False
    #if move is one space forward
    if verifying == False:
        if inital[1] == final[1] and inital[0] - final[0] == 1:
            if myBoard.get_piece((final[0], final[1])) == "0":
                return True
    #check en passant
    if verifying == False:
        if inital[0] == 5 and final[0] == 4 and abs(inital[1] - final[1]) == 1:
            if myBoard.get_piece((inital[0], final[1])) == "p" and myGame.black_valid_en_passant == (True,final[1]):
                return True
    
    #if move is diagonal CHECK
    if abs(inital[1] - final[1]) == 1 and inital[0] - final[0] == 1:
        if verifying == True:
            return True
        if myBoard.get_piece((final[0], final[1])).islower():
            return True
    return False
def pawn_black_validate(move, myGame,verifying):
    myBoard = myGame.board
    inital = move[0]
    final = move[1]
    #check if final doesn't have it's own players piece
    if verify_own_piece(move, myBoard) == False:
        return False
    #if move is two spaces forward
    if verifying == False:
        if inital[1] == final[1] and final[0]-inital[0] == 2:
            if inital[0] == 3:
                #check if there is a piece in the way
                if myBoard.get_piece((inital[0] + 1, inital[1])) != "0" or myBoard.get_piece((inital[0] + 2, inital[1])) != "0":
                    return False
                return True
            return False
    #if move is one space forward
    if verifying == False:
        if inital[1] == final[1] and final[0] - inital[0] == 1:
            if myBoard.get_piece((final[0], final[1])) == "0":
                return True
    #check en passant
    if verifying == False:
        if inital[0] == 6 and final[0] == 7 and abs(inital[1] - final[1]) == 1:
            if myBoard.get_piece((inital[0], final[1])) == "P" and myGame.white_valid_en_passant == (True,final[1]):
                return True
    #if move is diagonal CHECK
    if abs(inital[1] - final[1]) == 1 and final[0] - inital[0] == 1:
        if verifying == True:
            return True
        if myBoard.get_piece((final[0], final[1])).isupper():
            return True
    return False
def rook_validate(move, myBoard):
    inital = move[0]
    final = move[1]
    #check if final doesn't have it's own players piece
    if verify_own_piece(move, myBoard) == False:
        return False    
    #check column
    if inital[1] == final[1]:
        #check if there is a piece in the way
        column = final[1]
        if final[0] > inital[0]:
            direction = 1
        else:
            direction = -1
        for i in range(inital[0]+direction,final[0],direction):
            if myBoard.get_piece((i,column)) != "0":
                return False
        return True
    #check column
    if inital[0] == final[0]:
        #check if there is a piece in the way
        column = final[0]
        if final[1] > inital[1]:
            direction = 1
        else:
            direction = -1
        for i in range(inital[1]+direction,final[1],direction):
            if myBoard.get_piece((column,i)) != "0":
                return False
        return True
    return False
def knight_validate(move, myBoard):
    inital = move[0]
    final = move[1]
    #check if final doesn't have it's own players piece
    if verify_own_piece(move, myBoard) == False:
        return False
    #check if move is valid
    if abs(inital[0] - final[0]) == 2 and abs(inital[1] - final[1]) == 1:
        return True
    if abs(inital[0] - final[0]) == 1 and abs(inital[1] - final[1]) == 2:
        return True
    return False
def bishop_validate(move, myBoard):
    inital = move[0]
    final = move[1]
    #check that final spot doesn't have own piece
    if verify_own_piece(move, myBoard) == False:
        return False
    #check if move is valid
    if abs(inital[0] - final[0]) != abs(inital[1] - final[1]):
        return False
    #check if there is a piece in the way
    row = inital[0]
    column = inital[1]
    if final[0] > inital[0]:
        row_direction = 1
    else:
        row_direction = -1
    if final[1] > inital[1]:
        column_direction = 1
    else:
        column_direction = -1
    for i in range(1, abs(inital[0] - final[0])): #EDIT - check logic
        if myBoard.get_piece((row + i*row_direction, column + i*column_direction)) != "0":
            return False
    return True
def queen_validate(move, myBoard, myGame):
    #Queen is basically rook+bishop so just use both functions to verify
    diagonal = bishop_validate(move, myBoard)
    #print("diagonal")
    #print(diagonal)
    straight = rook_validate(move, myBoard)
    #print("straight")
    #print(straight)
    if diagonal or straight:
        return True
    return False
def king_validate(move, myGame,verifying):
    inital = move[0]
    final = move[1]
    myBoard = myGame.board
    turn = myGame.turn
    #check that final spot doesn't have own piece
    if verify_own_piece(move, myBoard) == False:
        #print("Own piece here")
        return False
    #check if moving into check
    if verifying == False:
        capturing_pieces = "upper" if turn == "black" else "lower"
        if can_piece_be_captured(final, myGame,capturing_pieces) == True:
            #print("Cannot move into check")
            return False
    #check for castling
    if turn == "white":
        if inital[0] == 9 and inital[1] == 6:
            if final[0] == 9 and final[1] == 4:
                if can_piece_be_captured(inital, myGame,"lower") == True:
                    #print("Cannot castle while in check")
                    return False
                if can_piece_be_captured((9,5), myGame,"lower") == True:
                    #print("Cannot castle through in check")
                    return False
                if myBoard.get_piece((9, 5)) == "0" and myBoard.get_piece((9, 4)) == "0" and myBoard.get_piece((9, 3)) == "0" and myBoard.get_piece((9, 2)) == "R":
                    if myGame.white_valid_castling == True and myGame.upper_left_rook_moved == -1:
                        return True
                return False
            if final[0] == 9 and final[1] == 8:
                if can_piece_be_captured(inital, myGame,"lower") == True:
                    #print("Cannot castle while in check")
                    return False
                if can_piece_be_captured((9,7), myGame,"lower") == True:
                    #print("Cannot castle through in check")
                    return False
                if myBoard.get_piece((9, 7)) == "0" and myBoard.get_piece((9, 8)) == "0" and myBoard.get_piece((9, 9)) == "R":
                    if myGame.white_valid_castling == True and myGame.upper_right_rook_moved == -1:
                        return True
                return False
    if turn == "black":
        if inital[0] == 2 and inital[1] == 6:
            if final[0] == 2 and final[1] == 4:
                if can_piece_be_captured(inital, myGame,"Upper") == True:
                    #print("Cannot castle while in check")
                    return False
                if can_piece_be_captured((2,5), myGame,"Upper") == True:
                    #print("Cannot castle through in check")
                    return False
                if myBoard.get_piece((2, 5)) == "0" and myBoard.get_piece((2, 4)) == "0" and myBoard.get_piece((2, 3)) == "0" and myBoard.get_piece((2, 2)) == "r":
                    if myGame.black_valid_castling == True and myGame.lower_left_rook_moved == -1:
                        return True
                return False
            if final[0] == 2 and final[1] == 8:
                if can_piece_be_captured(inital, myGame,"Upper") == True:
                    #print("Cannot castle while in check")
                    return False
                if can_piece_be_captured((2,7), myGame,"Upper") == True:
                    #print("Cannot castle through in check")
                    return False
                if myBoard.get_piece((2, 7)) == "0" and myBoard.get_piece((2, 8)) == "0" and myBoard.get_piece((2, 9)) == "r":
                    if myGame.black_valid_castling == True and myGame.lower_right_rook_moved == -1:
                        return True
                return False
    #check if move is valid
    if abs(inital[0] - final[0]) <= 1 and abs(inital[1] - final[1]) <= 1:
        return True
    return False
def can_piece_be_captured(coordinate, myGame, upperORlower):
    myBoard = myGame.board
    for i in range(2,10):
        for j in range(2,10):
            if myBoard.get_piece((i,j)) != "0":
                piece = myBoard.get_piece((i,j))
                if piece.islower() and upperORlower == "lower":
                    if piece_validate(piece, ((i,j), coordinate), myGame,True) == True:
                        #print((i,j))
                        #print(coordinate)
                        #print("returnig true1")
                        #print(piece)
                        return True
                if piece.isupper() and upperORlower == "upper":
                    if piece_validate(piece, ((i,j), coordinate), myGame,True) == True:
                        #print(piece)
                        return True
    return False