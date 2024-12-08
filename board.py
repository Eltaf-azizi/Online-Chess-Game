from piece import Bishop
from piece import King
from piece import Knight
from piece import Pawn
from piece import Queen
from piece import Rook
from piece import Piece

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
       

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Rook(7, 6, "w")
        self.board[7][7] = Knight(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")


    def update_moves(self):
        for row in self.board:
            for piece in row:
                if piece is not None:
                    piece.update_valid_moves(self.board)

    def draw(self, win):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    self.board[i][j].draw(win)

    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    if self.board[i][j].color != color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)
        return danger_moves


    def is_checked(self, color):
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    if self.board[i][j].king and self.board[i][j].color == color:
                        king_pos = (j, i)

        print(king_pos, danger_moves)
        if king_pos in danger_moves:
            return True
        return False

    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    if self.board[i][j].selected:
                        prev = (i, j)

        # if piece
        if self.board[row][col] is None:
            moves = self.board[prev[0]][prev[1]].move_list
            if (col, row) in moves:

                changed = self.move(prev, (row, col), color)
            

        else:
            if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                moves = self.board[prev[0]][prev[1]].move_list
                if (col, row) in moves:
                    changed = self.move(prev, (row, col), color)

                if self.board[row][col].color == color:
                    self.board[row][col].selected = True
                    

            else:
                self.reset_selected()
                if self.board[row][col].color == color:
                    self.board[row][col].selected = True

        return changed

    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] is not None:
                    self.board[i][j].selected = False

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self.board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = None
        self.board = nBoard


        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            changed = False
            nBoard = self.board[:]
            if nBoard[start[0]][start[1]].pawn:
                nBoard[start[0]][start[1]].first = True

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = None
            self.board = nBoard
        
        else:
            self.reset_selected()



        self.update_moves()
        return changed
