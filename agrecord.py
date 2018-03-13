'''
Created on 2018/03/13

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

class Main:
    def __init__(self):
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0 # used to store y coordinate of mouse event
        pygame.display.set_caption('Agrecord')
        self.mainboard = actionboard.Actionboard()
        self.players = []
        for p in GLINK:
            self.players.append(playerboard.PlayerBoard(*p))
        self.perspectivePlayer = self.players[0]
        self.perspective = 'page1'
        self.DISPLAYSURF.fill(BGCOLOR)
        self.drawPage1()
        self.mouseClicked = False
        self.clickedBox = 16
        
    def gameStart(self):
        while True: # main game loop
            self.mouseClicked = False
            self.mainboard.actionRect.clear()
            self.DISPLAYSURF.fill(BGCOLOR) # drawing the window
            #描画するページについての分岐
            if self.perspective == 'page1':
                self.drawPage1()
            elif self.perspective == 'page2':
                self.drawPage2()
            else:
                self.drawfarmyard()
        
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    self.mouseClicked = True
                    
            if self.mouseClicked == True:
                for space in self.mainboard.actionRect:
                    if space.collidepoint(self.mousex,self.mousey) == True:
                        self.clickedBox = self.mainboard.actionRect.index(space)
                        pygame.draw.rect(self.DISPLAYSURF,BLACK,(0,0,20,20))
            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)
    def drawPage1(self):
        triangle = ((WINDOWWIDTH-int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(WINDOWWIDTH-int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(WINDOWWIDTH-int(XMARGIN/5),int(WINDOWHEIGHT/2)))
        pygame.draw.polygon(self.DISPLAYSURF,HIGHLIGHTCOLOR,triangle)
        for player in self.players:
            pygame.draw.circle(self.DISPLAYSURF, player.playercolor, ((self.players.index(player)*2+1)*int((WINDOWWIDTH-2*XMARGIN)/10)+XMARGIN, WINDOWHEIGHT-int(BOXSIZE/2)), 30, 0)
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left,top = leftTopCoordsOfBox(boxx, boxy)
                self.mainboard.actionRect.append(pygame.draw.rect(self.DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE)))
                fontObj = pygame.font.Font('ipag.ttf',BOARDLETTERSIZE)
                words = self.mainboard.actionCards[boxx*3+boxy].name.split()
                for word in words:
                    textSurfaceObj = fontObj.render(word,True,BLACK,BACKLETTER)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (left+int(BOXSIZE/2), words.index(word)*BOARDLETTERSIZE+top+int(BOXSIZE/4))
                    self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                if self.mainboard.actionCards[boxx*3+boxy].meeple != None:
                    pygame.draw.circle(self.DISPLAYSURF, player.playercolor, (left+int(BOXSIZE/2),top+int(BOXSIZE*3/4) ), 20, 0)
                    #meepleImg = pygame.image.load('Meeple.png').convert_alpha()
                    #meepleImg.fill(mainboard.actionCards[boxx*3+boxy].meeple.playercolor)
                    #DISPLAYSURF.blit(meepleImg, (left+int(BOXSIZE/2), top+int(BOXSIZE/2)))
    def drawPage2(self):
        triangle = ((int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(int(XMARGIN/5),int(WINDOWHEIGHT/2)))
        pygame.draw.polygon(self.DISPLAYSURF,HIGHLIGHTCOLOR,triangle)
        for player in self.players:
            pygame.draw.circle(self.DISPLAYSURF, player.playercolor, ((self.players.index(player)*2+1)*int((WINDOWWIDTH-2*XMARGIN)/10)+XMARGIN, WINDOWHEIGHT-int(BOXSIZE/2)), 30, 0)
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left,top = leftTopCoordsOfBox(boxx, boxy)
                self.mainboard.actionRect.append(pygame.draw.rect(self.DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE)))
                fontObj = pygame.font.Font('ipag.ttf',BOARDLETTERSIZE)
                words = self.mainboard.actionCards[14+boxx*3+boxy].name.split()
                for word in words:
                    textSurfaceObj = fontObj.render(word,True,BLACK,BACKLETTER)
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (left+int(BOXSIZE/2), words.index(word)*BOARDLETTERSIZE+top+int(BOXSIZE/4))
                    self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
                if self.mainboard.actionCards[14+boxx*3+boxy].meeple != None:
                    pygame.draw.circle(self.DISPLAYSURF, player.playercolor, (left+int(BOXSIZE/2),top+int(BOXSIZE*3/4) ), 20, 0)
                    #meepleImg = pygame.image.load('Meeple.png').convert_alpha()
                    #meepleImg.fill(mainboard.actionCards[boxx*3+boxy].meeple.playercolor)
                    #DISPLAYSURF.blit(meepleImg, (left+int(BOXSIZE/2), top+int(BOXSIZE/2)))
    def drawfarmyard(self):
        triangle = ((int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(int(XMARGIN/5),int(WINDOWHEIGHT/2)))
        pygame.draw.polygon(self.DISPLAYSURF,HIGHLIGHTCOLOR,triangle)
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT):
                left,top = leftTopCoordsOfBox(boxx, boxy)
                self.mainboard.actionRect.append(pygame.draw.rect(self.DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE)))
                #pygame.draw.rect(DISPLAYSURF,WOODY,leftTopCoordsOfBox(0,1))
                #pygame.draw.rect(DISPLAYSURF,WOODY,leftTopCoordsOfBox(0,2))
def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

if __name__ == "__main__":
    m = Main()
    m.gameStart()