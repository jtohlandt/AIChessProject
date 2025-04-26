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
        
        self.board[2] = ["8","|","r", "n", "b", "q", "k", "b", "n", "r", "|","8"]
        self.board[9] = ["1","|","R", "N", "B", "Q", "K", "B", "N", "R","|","1"]
        for i in range(2,10):
            self.board[3][i] = "p"
        for i in range(2,10):
            self.board[8][i] = "P"
            
    def print_board(self):
        for i in range(12):
            for j in range(12):
                print(self.board[i][j], end = " ")
            print()
    def get_piece(self, position):
        #print(self.board[position[0]][position[1]])
        return self.board[position[0]][position[1]]
