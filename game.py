import pygame
import os
from piece import Bishop
from board import Board
import time
pygame.font.init()


board = pygame.transform.scale(pygame.image.load(os.path.join("image", "board_alt.png")), (750, 750))
rect = (113, 113, 525, 525)



def redraw_gameWindow(win, bo, p1, p2):

    win.blit(board, (0, 0))
    bo.draw(win)

    formatTime1 = str(p1 // 60) + ":" + str(p1 % 60)
    formatTime2 = str(p2 // 60) + ":" + str(p2 % 60)

    if p1 % 60 == 0:
        formatTime1 += "0"
    if p2 % 60 == 0:
        formatTime2 += "0"

    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render("Player 2 Time: " + str(formatTime2), 1, (255, 255, 255))
    txt2 = font.render("Player 1 Time: " + str(formatTime1), 1, (255, 255, 255))
    win.blit(txt, (540, 10))
    win.blit(txt2, (540, 700))

    pygame.display.update()



def end_screen(win, text):

    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text, 1, (255, 0, 0))
    win.blit(txt, (width/2 - txt.get_width()/2, 300))
    pygame.display.update()

    pygame.set_timer(pygame.USEREVENT+1, 3000)


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False

            elif event.type == pygame.KEYDOWN:
                run = False

            elif event.type == pygame.USEREVENT+1:
                run = False



def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]

    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            
            divX = x - rect[0]
            divY = y - rect[0]
            i = int(divX / (rect[2]/8))
            j = int(divY / (rect[3]/8))
            return i, j




def main():
    p1Time = 900  # Set initial time for Player 1 (15 minutes)
    p2Time = 900  # Set initial time for Player 2 (15 minutes)
    turn = "w"  # White starts
    bo = Board()  # Create a new Board object (no arguments needed)
    bo.update_moves()  # Update all the moves of the pieces
    clock = pygame.time.Clock()  # Create a clock object to manage the frame rate
    run = True
    startTime = time.time()  # Start the timer

    while run:
        clock.tick(10)  # Run at 10 frames per second

        # Update player time based on turn
        if turn == "w":
            p1Time -= time.time() - startTime  # Decrease time for Player 1
        else:
            p2Time -= time.time() - startTime  # Decrease time for Player 2

        startTime = time.time()  # Reset start time for the next frame

        # Redraw the game window with the updated board and times
        redraw_gameWindow(win, bo, int(p1Time), int(p2Time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            # Handle mouse click events to select and move pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bo.update_moves()  # Update valid moves for each piece
                i, j = click(pos)  # Get the clicked square's coordinates
                change = bo.select(i, j, turn)  # Try to select and move the piece
                bo.update_moves()  # Update valid moves again after the move

                if change:
                    startTime = time.time()  # Reset the timer if a move occurred
                    # Change turn to the other player
                    if turn == "w":
                        turn = "b"
                    else:
                        turn = "w"

        # Check if either player has won (checkmate)
        if bo.checkMate("w"):
            end_screen(win, "Black Wins!")  # White is checkmated, black wins

        elif bo.checkMate("b"):
            end_screen(win, "White Wins!")  # Black is checkmated, white wins


width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
main()