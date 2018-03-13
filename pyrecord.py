'''
Created on 2018/03/06

@author: Yuya
'''
import pygame,sys,actionboard,playerboard
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 800 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
BOXSIZE = 120 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 5 # number of columns of icons
BOARDHEIGHT = 3 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
BLACK    = (  0,   0,   0)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
LEAFGREEN= (109, 224,  81)
WOODY    = (158,  79,  45)
GLINK = (('赤',1,RED),('オスマン',2,BLUE),('ニノ',3,ORANGE),('ぐれそ',4,PURPLE),('シゲヨシ',5,GRAY))

BGCOLOR =  (196 ,227,  32)
LIGHTBGCOLOR = GRAY
BOXCOLOR = (110, 189,  15)
HIGHLIGHTCOLOR = (93,127,26)
BACKLETTER = (246,234,44)
BOARDLETTERSIZE = 24

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Agrecord')
    mainboard = actionboard.Actionboard()
    players = []
    for p in GLINK:
        players.append(playerboard.PlayerBoard(*p))
    perspectivePlayer = players[0]
    perspective = mainboard
        
    DISPLAYSURF.fill(BGCOLOR)
    drawPage1(mainboard, players)
    mouseClicked = False
        
    while True: # main game loop
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        #perspective.drawGraphic(pygame,DISPLAYSURF,perspectivePlayer)
        drawPage1(mainboard, players)
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        
        
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPage1(mainboard,players):
    triangle = ((WINDOWWIDTH-int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(WINDOWWIDTH-int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(WINDOWWIDTH-int(XMARGIN/5),int(WINDOWHEIGHT/2)))
    pygame.draw.polygon(DISPLAYSURF,HIGHLIGHTCOLOR,triangle)
    for player in players:
        pygame.draw.circle(DISPLAYSURF, player.playercolor, ((players.index(player)*2+1)*int((WINDOWWIDTH-2*XMARGIN)/10)+XMARGIN, WINDOWHEIGHT-int(BOXSIZE/2)), 30, 0)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            fontObj = pygame.font.Font('ipag.ttf',BOARDLETTERSIZE)
            words = mainboard.actionCards[boxx*3+boxy].name.split()
            for word in words:
                textSurfaceObj = fontObj.render(word,True,BLACK,BACKLETTER)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (left+int(BOXSIZE/2), words.index(word)*BOARDLETTERSIZE+top+int(BOXSIZE/4))
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
            if mainboard.actionCards[boxx*3+boxy].meeple != None:
                pygame.draw.circle(DISPLAYSURF, player.playercolor, (left+int(BOXSIZE/2),top+int(BOXSIZE*3/4) ), 20, 0)
                    #meepleImg = pygame.image.load('Meeple.png').convert_alpha()
                    #meepleImg.fill(mainboard.actionCards[boxx*3+boxy].meeple.playercolor)
                    #DISPLAYSURF.blit(meepleImg, (left+int(BOXSIZE/2), top+int(BOXSIZE/2)))
def drawPage2(mainboard,players):
    triangle = ((int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(int(XMARGIN/5),int(WINDOWHEIGHT/2)))
    pygame.draw.polygon(DISPLAYSURF,HIGHLIGHTCOLOR,triangle)
    for player in players:
        pygame.draw.circle(DISPLAYSURF, player.playercolor, ((players.index(player)*2+1)*int((WINDOWWIDTH-2*XMARGIN)/10)+XMARGIN, WINDOWHEIGHT-int(BOXSIZE/2)), 30, 0)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            fontObj = pygame.font.Font('ipag.ttf',BOARDLETTERSIZE)
            words = mainboard.actionCards[14+boxx*3+boxy].name.split()
            for word in words:
                textSurfaceObj = fontObj.render(word,True,BLACK,BACKLETTER)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (left+int(BOXSIZE/2), words.index(word)*BOARDLETTERSIZE+top+int(BOXSIZE/4))
                DISPLAYSURF.blit(textSurfaceObj, textRectObj)
            if mainboard.actionCards[boxx*3+boxy].meeple != None:
                pygame.draw.circle(DISPLAYSURF, player.playercolor, (left+int(BOXSIZE/2),top+int(BOXSIZE*3/4) ), 20, 0)
                #meepleImg = pygame.image.load('Meeple.png').convert_alpha()
                #meepleImg.fill(mainboard.actionCards[boxx*3+boxy].meeple.playercolor)
                #DISPLAYSURF.blit(meepleImg, (left+int(BOXSIZE/2), top+int(BOXSIZE/2)))
def drawfarmyard(mainboard,viedplayer,parspectiveplayer):
    triangle = ((int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(int(XMARGIN/5),int(WINDOWHEIGHT/2)))
    pygame.draw.polygon(DISPLAYSURF,HIGHLIGHTCOLOR,triangle)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = leftTopCoordsOfBox(boxx, boxy)
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
    #pygame.draw.rect(DISPLAYSURF,WOODY,leftTopCoordsOfBox(0,1))
    #pygame.draw.rect(DISPLAYSURF,WOODY,leftTopCoordsOfBox(0,2))
def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

if __name__ == '__main__':
    main()