from my_chess.board import board
from my_chess.move import process_move
from my_chess.move import process_move_ai
from my_chess.move import is_checkmate_stalemate
from my_chess.ai import ai_move

class game:
    def __init__(self):
        self.game_stack = []
        
        self.mode = "NotSet"
        self.turn_num = 0
        self.previous_turn = []
        self.board = board()
        self.turn = "white"
        self.white_valid_castling = True
        self.black_valid_castling = True
        self.white_king_coordinates = (9,6)
        self.black_king_coordinates = (2,6)
        self.upper_left_rook_moved = -1
        self.upper_right_rook_moved = -1
        self.lower_left_rook_moved = -1
        self.lower_right_rook_moved = -1
        white_column = -1
        self.white_valid_en_passant = (False, white_column)
        black_column = -1
        self.black_valid_en_passant = (False, black_column)


    def run(self):
        while self.mode == "AI":
            self.board.print_board()
            status = is_checkmate_stalemate(self, self.turn)
            if status == 1:
                print("{self.turn} is in checkmate".format(self=self))
                break
            if status == 2:
                print("{self.turn} is in stalemate".format(self=self))
                break
            if status == 3:
                print("{self.turn} is in check".format(self=self))
            if self.turn == "white":
                move = input("Enter your move {self.turn}: ".format(self=self))
                if move == "q":
                    break
                if len(move) != 4:
                    print("Move must be 4 characters long")
                    continue
                process_move(move, self)
                continue
            if self.turn == "black":
                print("AI is thinking...")
                move = ai_move(self)
                print("AI move: {move}".format(move=move))
                process_move_ai(move,self)
        
        while self.mode == "Player":
            self.board.print_board()
            status = is_checkmate_stalemate(self, self.turn)
            if status == 1:
                print("{self.turn} is in checkmate".format(self=self))
                break
            if status == 2:
                print("{self.turn} is in stalemate".format(self=self))
                break
            if status == 3:
                print("{self.turn} is in check".format(self=self))
            move = input("Enter your move {self.turn}: ".format(self=self))
            if move == "q":
                break
            if len(move) != 4:
                print("Move must be 4 characters long")
                continue
            process_move(move, self)

    def set_mode(self):
        while True:
            mode = input("Type AI to play against the AI or type Player to play 2 player: ")
            if mode == "AI":
                self.mode = mode
                break
            if mode == "Player":
                self.mode = mode
                break
            print("Invalid mode")
            continue