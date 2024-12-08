import pygame
import os
from piece import Bishop
from board import Board
import time
pygame.font.init()


board = pygame.transform.scale(pygame.image.load(os.path.join("image", "board_alt.png")), (750, 750))
rect = (113, 113, 525, 525)

turn = "w"

def menu_screen(win):
    run = True

    while run: 
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 80)
        title = font.render("Online Chess!", 1, (0, 128, 0))
        win.blit(title, (width/2 - title.get_width()/2, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False


    main()


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
            divY = y - rect[1]
            i = int(divX / (rect[2]/8))
            j = int(divY / (rect[3]/8))
            return i, j

    return -1, -1


def main():

    global turn
    p1Time = 900  
    p2Time = 900  
    count = 0
    bo = Board()  
    bo.update_moves()  
    clock = pygame.time.Clock()  
    run = True
    startTime = time.time()  

    while run:
        clock.tick(15) 

        
        if turn == "w":
            p1Time -= time.time() - startTime 
            if p1Time <= 0:
                end_screen(win, "Black Wins") 
        else:
            p2Time -= time.time() - startTime 
            if p2Time <= 0:
                end_screen(win, "White Wins")

        startTime = time.time()  


        redraw_gameWindow(win, bo, int(p1Time), int(p2Time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bo.update_moves() 
                i, j = click(pos)  
                change = bo.select(i, j, turn)

                if change == True:
                    startTime = time.time()  
                    count += 1
                    
                    if turn == "w":
                        turn = "b"
                        bo.reset_selected()
                    else:
                        turn = "w"
                        bo.reset_selected()

    menu_screen()
        
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
# bo, color = connect()
menu_screen(win)