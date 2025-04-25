class board:
    def __init__(self):
        self.board = [["0" for i in range(12)] for j in range(12)]
        self.board[0] = ["/"] + ["-"] + ["a", "b", "c", "d", "e", "f", "g", "h"] + ["-"] + ["\\"]
        self.board[1] = ["|"] +["-"] * 10 + ["|"]
        self.board[10] = ["|"] +["-"] * 10 + ["|"]
        self.board[11] = ["\\"] + ["-"] + ["a", "b", "c", "d", "e", "f", "g", "h"] + ["-"] + ["/"]
        for i in range(2,10):
            self.board[i][1] = "|"
            self.board[i][10] = "|"
        for i in range(2,10):
            self.board[i][0] = 8-i + 2
            self.board[i][11] = 8-i +2 
        #2 player demo
        '''
        self.board[2] = ["8","|","R", "N", "B", "Q", "K", "B", "N", "R", "|","8"]
        self.board[9] = ["1","|","r", "n", "b", "q", "k", "b", "n", "r","|","1"]
        for i in range(2,10):
            self.board[3][i] = "P"
        for i in range(2,10):
            self.board[8][i] = "p"
        '''
        #pawn promotion demo
        '''
        self.board[2] = ["8","|","R", "N", "B", "Q", "K", "B", "N", "R", "|","8"]
        self.board[9] = ["1","|","0", "n", "b", "q", "k", "b", "n", "r","|","1"]
        for i in range(3,10):
            self.board[3][i] = "P"
        for i in range(3,10):
            self.board[8][i] = "p"
        self.board[8][2] = "P"
        '''
        #castling demo
        '''
        self.board[2] = ["8","|","R", "0", "0", "0", "K", "B", "N", "R", "|","8"]
        self.board[9] = ["1","|","r", "n", "b", "q", "k", "b", "n", "r","|","1"]
        for i in range(2,10):
            self.board[3][i] = "P"
        for i in range(2,10):
            self.board[8][i] = "p"
        '''
        
        #AI avoiding check demo
        self.board[2] = ["8","|","R", "N", "B", "Q", "K", "Q", "N", "R", "|","8"]
        self.board[9] = ["1","|","0", "0", "0", "0", "k", "0", "0", "0","|","1"]
        
        #AI capturing piece demo
        '''
        self.board[2] = ["8","|","R", "N", "B", "Q", "K", "B", "Q", "R", "|","8"]
        self.board[9] = ["1","|","r", "n", "b", "q", "k", "b", "n", "r","|","1"]
        for i in range(2,10):
            self.board[3][i] = "P"
        for i in range(2,10):
            self.board[8][i] = "p"
        self.board[3][8] = "0"
        '''
            
    def print_board(self):
        for i in range(12):
            for j in range(12):
                print(self.board[i][j], end = " ")
            print()
    def get_piece(self, position):
        #print(self.board[position[0]][position[1]])
        return self.board[position[0]][position[1]]
