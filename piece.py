import pygame
import os


board = pygame.transform.scale2x(pygame.image.load(os.path.join("image", "board_alt.png")))


b_bishop = pygame.image.load(os.path.join("image", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("image", "black_king.png"))
b_knight = pygame.image.load(os.path.join("image", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("image", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("image", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("image", "black_rook.png"))



w_bishop = pygame.image.load(os.path.join("image", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("image", "white_king.png"))
w_knight = pygame.image.load(os.path.join("image", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("image", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("image", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("image", "white_rook.png"))


b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []


for img in b:
    B.append(pygame.transform.scale(img, (65, 65)))


for img in w:
    W.append(pygame.transform.scale(img, (65, 65)))





class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False



    def isSelected(self):
        return self.selected
    

    def update_valid_moves(self):
        self.move_list = self.valid_moves(board)
    


    def draw(self, win):
                
        if self.color == "w":
            drawThis = W[self.img]
        
        else:
            drawThis = B[self.img]


        if self.selected:
            moves = self.move_list

            for move in moves:
                x = 5 + round(self.startX + (move[0] * self.rect[2]/8))
                y = 5 + round(self.startY + (move[1] * self.rect[3]/8))
                pygame.draw.circle(win, (255, 0, 0), 10)


        x = 5 + round(self.startX + (self.col * self.rect[2]/8))
        y = 5 + round(self.startY + (self.row * self.rect[3]/8))


        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 55, 55), 2)
            

        win.blit(drawThis, (x, y))



    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]



    def __str__(self):
        return str(self.col) + " " + str(self.row)



class Bishop(Piece):
    img = 0


    def valid_moves(self, board):
       
        i = self.row
        j = self.col

        moves = []


        # TOP RIGHT
        djL = j + 1
        djR = j - 1

        for di in range(i-1, -1, -1):
            if djL < 8:
                p = board[di][djL]

                if p == 0:
                    moves.append((djL, di))

                elif p.color != self.color:
                    moves.append((djL, di))
                    break

                else:
                    break

            else:
                break

            djL += 1


        for di in range(i -1, -1, -1):
            if djR > -1:
                p = board[di][djR]

                if p == 0:
                    moves.append((djR, di))

                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1



        
        # TOP LEFT

        djL = j + 1
        djR = j - 1

        for di in range(i+1, 8):
            if djL < 8:
                p = board[di][djL]

                if p == 0:
                    moves.append((djL, di))

                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                
                else:
                    break
            else:
                break

            djL += 1



            if djR > -1:
                p = board[di][djR]

                if p == 0:
                    moves.append((djR, di))

                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        return moves



class King(Piece):
    img = 1


    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True




    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []


        if i > 0:

        # TOP LEFT
            if j > 0:
                p = board[i-1][j-1]
                if p == 0:
                    moves.append((j - 1, i - 1))
                elif p.color != self.color:
                    moves.append((j-1, i-1))


        # TOP MIDDLE
            p = board[i-1][j]
            if p == 0:
                moves.append((j, i - 1))
            elif p.color != self.color:
                moves.append((j, i-1))


        # TOP RIGHT
            if j < 7:
                p = board[i-1][j+1]
                if p == 0:
                    moves.append((j + 1, i - 1))
                elif p.color != self.color:
                    moves.append((j+1, i-1))

        
        if i < 7:
        # BOTTOM LEFT
            if j > 0:
                p = board[i+1][j-1]
                if p == 0:
                    moves.append((j -1, i + 1))
                elif p.color != self.color:
                    moves.append((j-1, i+1))


        # BOTTOM MIDDLE
            p = board[i+1][j]
            if p == 0:
                moves.append((j, i + 1))
            elif p.color != self.color:
                moves.append((j, i+1))


        # BOTTOM RIGHT
            if j < 7:
                p = board[i+1][j+1]
                if p == 0:
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:
                    moves.append((j+1, i+1))


        # MIDDLE LEFT
        if j > 0:
            p = board[i][j-1]
            if p == 0:
                moves.append((j - 1, i))
            elif p.color != self.color:
                moves.append((j-1, i))


        # MIDDLE RIGHT
        if j < 7:
            p = board[i][j+1]
            if p == 0:
                moves.append((j + 1, i))
            elif p.color != self.color:
                moves.append(j+1, i)


        return moves


class Knight(Piece):
    img = 2

    def valid_moves(self, board):

        i = self.row
        j = self.col


        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            p = board[i + 2][j-1]
            if p == 0:
                moves.append((j-1, i + 2))
            elif p.color != self.color:
                moves.append((j-1, i+2))


        # UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j-1]
            if p == 0:
                moves.append((j-1, i - 2))
            elif p.color != self.color:
                moves.append((j-1, i-2))


        # DOWN RIGHT
        if i < 6 and j > 7:
            p = board[i + 2][j+1]
            if p == 0:
                moves.append((j + 1, i + 2))
            elif p.color != self.color:
                moves.append((j+1, i+2))


        
        # UP RIGHT
        if i > 1 and j < 7:
            p = board[i - 2][j+1]
            if p == 0:
                moves.append((j + 1, i - 2))
            elif p.color != self.color:
                moves.append((j+1, i-2))



        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == 0:
                moves.append(j - 2,  - 1)

            elif p.color != self.color:
                moves.append((j - 2, i - 1))


        
        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p == 0:
                moves.append(j + 2,  - 1)

            elif p.color != self.color:
                moves.append((j + 2, i - 1))

        

        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p == 0:
                moves.append(j - 2,  + 1)

            elif p.color != self.color:
                moves.append((j - 2, i + 1))



        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p == 0:
                moves.append(j + 2,  + 1)

            elif p.color != self.color:
                moves.append((j + 2, i + 1))



        return moves




class Pawn(Piece):
    img = 3

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.first = True
        self.queen = False
        self.pawn = True


    def valid_moves(self, board):
        
        i = self.row
        j = self.col


        moves = []

        if self.color == "b":

            if i < 7:
                p = board[i+1][j]
                if p == 0:
                    moves.append((j, i+1))


                    # DIAGONAL
                    if j < 7:
                        p = board[i+1][j+1]
                        if p != 0:
                            if p.color != self.color:
                                moves.append((j+1, i+1))


                    if j > 7:
                        p = board[i+1][j-1]
                        if p != 0:
                            if p.color != self.color:
                                moves.append((j-1, i+1))


            if self.first:
                if i < 6:
                    p = board[i+2][j]
                    if p == 0:
                        if board[i+1][j] == 0:
                            moves.append((j, i+2))

                    elif p.color != self.color:
                        moves.append((j, i+2))


        # WHITE
        else:

            if i > 0:
                p = board[i - 1][j]
                if p == 0:
                    moves.append((j, i - 1))



            if j < 7:
                p = board[i - 1][j + 1]
                if p != 0:
                    if p.color != self.color:
                        moves.append((j + 1, i - 1))


            if j > 0:
                p = board[i-1][j-1]
                if p != 0:
                    if p.color != self.color:
                        moves.append((j-1, i-1))

            
            if self.first:

                if i > 1:
                    p = board[i - 2][j]
                    if p == 0:
                        if board[i+1][j] == 0:
                            moves.append((j, i - 2))
                    
                    elif p.color != self.color:
                        moves.append((j, i - 2))


        return moves




class Queen(Piece):

    img = 4


    def valid_moves(self, board):
       
        i = self.row
        j = self.col

        moves = []


        # TOP RIGHT
        djL = j + 1
        djR = j - 1

        for di in range(i-1, -1, -1):
            if djL < 8:
                p = board[di][djL]

                if p == 0:
                    moves.append((djL, di))

                elif p.color != self.color:
                    moves.append((djL, di))
                    break

                else:
                    djL = 9

            djL += 1



            if djR > -1:
                p = board[di][djR]

                if p == 0:
                    moves.append((djR, di))

                elif p.color != self.color:
                    moves.append((djR, di))
                    break

                else:
                    djR = -1

            djR -= 1



        
        # TOP LEFT

        djL = j + 1
        djR = j - 1

        for di in range(i+1, 8):
            if djL < 8:
                p = board[di][djL]

                if p == 0:
                    moves.append((djL, di))

                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break

            djL += 1



            if djR > -1:
                p = board[di][djR]

                if p == 0:
                    moves.append((djR, di))

                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break

            djR -= 1

        # UP
        for x in range(i-1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break


        # DOWN
        for x in range(i+1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break


        # LEFT
        for x in range(j-1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break


        # RIGHT
        for x in range(j+1, 8, 1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break


        return moves

            

class Rook(Piece):
    img = 5



    def valid_moves(self, board):

        i = self.row
        j = self.col

        moves = []


        # UP
        for x in range(i-1, -1, -1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break


        # DOWN
        for x in range(i+1, 8, 1):
            p = board[x][j]
            if p == 0:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break


        # LEFT
        for x in range(j-1, -1, -1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break


        # RIGHT
        for x in range(j+1, 8, 1):
            p = board[i][x]
            if p == 0:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        return moves