'''
Created on 2018/03/13

@author: Yuya
'''
import pygame,sys,actionboard,playerboard
from pygame.locals import *

FPS = 20 # frames per second, the general speed of the program
WINDOWWIDTH = 800 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
BOXSIZE = 120 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 5 # number of columns of icons
BOARDHEIGHT = 3 # number of rows of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

RESOURCE = ('木','煉瓦','葦','石','飯','小麦','野菜','羊','猪','牛','点')

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

BGCOLOR =  (196 ,227,  32)
LIGHTBGCOLOR = GRAY
BOXCOLOR = (110, 189,  15)
HIGHLIGHTCOLOR = (93,127,26)
BACKLETTER = (246,234,44)#文字背景色
BOARDLETTERSIZE = 24


GLINK = (('赤',1,RED),('オスマン',2,BLUE),('ニノ',3,ORANGE),('ぐれそ',4,PURPLE),('シゲヨシ',5,GRAY))


class Main:
    def __init__(self):
        #__init__はMainクラスのインスタンスが作られた時に呼び出されるメソッド
        pygame.init()#pygameインスタンスの初期化
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#一番大きなウィンドウの表示
        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0 # used to store y coordinate of mouse event
        pygame.display.set_caption('Agrecord')#ウィンドの上部に表示する名前
        self.mainboard = actionboard.Actionboard()
        #actionboard.pyをactionboardパッケージとしてimport。self.mainboardがActionboardクラスのインスタンス
        self.players = []
        for p in GLINK:
            self.players.append(playerboard.PlayerBoard(*p))
        #プレイヤー情報の代入(これはのちに改良する。今は適当
        self.perspectivePlayer = self.players[0]
        #盤を見ているプレイヤーを表す変数
        self.turnplayer = self.players[0]
        self.perspective = 6
        #プレイヤーが見ているボードがどのボードかを表す変数、0~4はplayers[0]~[4]に対応。6,7はpage1とpage2に対応。
        self.DISPLAYSURF.fill(BGCOLOR)
        #ボードをBGCOLORで満たす
        self.drawPage1()
        #Page1の描画
        self.mouseClicked = False
        
    def gameStart(self):
        #インスタンスが作成された時にこの関数がすぐに読み出されるようになっている。
        while True: #一番大きなゲームループ
            self.mouseClicked = False
            #マウスがクリックされているかどうかを示す変数
            self.mainboard.actionRect.clear()
            #3かける5の盤面のマスを格納する多重リスト。ここでは.clearで中身を消去している。
            self.mainboard.playerCirc.clear()
            #プレイヤーボタンを格納するリスト。ここでは.clearで中身を消去している。
            self.mainboard.pagecTri.clear()
            #ページ切り替えの三角ボタンを格納するリスト。ここでは.clearで中身を消去している。
            
            if self.mainboard.phase == '準備フェイズ':
                for actspace in self.mainboard.actionCards:
                    actspace.prepare()
                self.mainboard.phase = '労働フェイズ'
                
            self.DISPLAYSURF.fill(BGCOLOR) # drawing the window
            for player in self.players:
                self.mainboard.playerCirc.append(pygame.draw.circle(self.DISPLAYSURF, player.playercolor, ((self.players.index(player)*2+1)*int((WINDOWWIDTH-2*XMARGIN)/10)+XMARGIN, WINDOWHEIGHT-int(BOXSIZE/2)), 30, 0))
            #プレイヤーの盤面に飛ぶプレイヤーボタンを作る処理
            fontObj = pygame.font.Font('ipag.ttf',BOARDLETTERSIZE)
            textSurfaceObj = fontObj.render('ラウンド'+str(self.mainboard.round)+'：'+self.mainboard.phase +'：手番'+ self.turnplayer.playername,True,BLACK,BACKLETTER)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (int(WINDOWWIDTH/2),int(YMARGIN/2))
            self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
            #ラウンドやフェイズ、手番情報を格納する変数
            triangle = ((WINDOWWIDTH-int(XMARGIN*4/5),int(WINDOWHEIGHT/2)+30),(WINDOWWIDTH-int(XMARGIN*4/5),int(WINDOWHEIGHT/2)-30),(WINDOWWIDTH-int(XMARGIN/5),int(WINDOWHEIGHT/2)))
            self.mainboard.pagecTri.append(pygame.draw.polygon(self.DISPLAYSURF,HIGHLIGHTCOLOR,triangle))
            #盤面移動の三角アイコンの作成
            for key, value in self.perspectivePlayer.supply.items():
                textSurfaceObj = fontObj.render(key+str(value),True,BLACK,BACKLETTER)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (int(XMARGIN/2), int(YMARGIN/2)+RESOURCE.index(key)*int((WINDOWHEIGHT-YMARGIN)/10))
                self.DISPLAYSURF.blit(textSurfaceObj, textRectObj)
            #プレイヤーのサプライ情報の表示
            #これ以下、描画するページについての分岐
            if self.perspective == 6:
                self.drawPage1()
            elif self.perspective == 7:
                self.drawPage2()
            elif self.perspective <= 4:
                self.drawfarmyard(self.players[self.perspective])
            # イベントを取り扱うループ
            for event in pygame.event.get(): 
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    self.mousex, self.mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    self.mousex, self.mousey = event.pos
                    self.mouseClicked = True
                    
            if self.mouseClicked == True:
                if self.mainboard.phase == '労働フェイズ':
                    for space in self.mainboard.actionRect:
                        if space.collidepoint(self.mousex,self.mousey) == True:
                            if self.perspective == 6:
                                self.mainboard.actionCards[self.mainboard.actionRect.index(space)].doAction(self.turnplayer)
                                self.mainboard.actionCards[self.mainboard.actionRect.index(space)].meeple = self.turnplayer.playercolor 
                            elif self.perspactive == 7:
                                self.mainboard.actionCards[self.mainboard.actionRect.index(space)-15].doAction(self.turnplayer)
                                self.mainboard.actionCards[self.mainboard.actionRect.index(space)-15].meeple = self.turnplayer.playercolor
                            self.turnplayer.workingMember += 1
                            if self.turnplayer == self.players[4]:
                                self.turnplayer = self.players[0]
                            else:
                                self.turnplayer = self.players[self.players.index(self.turnplayer)+1]
                for pmeeple in self.mainboard.playerCirc:
                    if pmeeple.collidepoint(self.mousex,self.mousey) == True:
                        self.perspective = self.mainboard.playerCirc.index(pmeeple)
                if self.mainboard.pagecTri[0].collidepoint(self.mousex,self.mousey) == True:
                    if self.perspective == 6:
                        self.perspective = 7
                    else:
                        self.perspective = 6
            # Redraw the screen and wait a clock tick.
            pygame.display.update()
            self.FPSCLOCK.tick(FPS)
    def drawPage1(self):
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
                if self.mainboard.actionCards[boxx*3+boxy].meeple is not None:
                    pygame.draw.circle(self.DISPLAYSURF,self.mainboard.actionCards[boxx*3+boxy].meeple, (left+int(BOXSIZE/2),top+int(BOXSIZE*3/4) ), 20, 0)
                  
    def drawPage2(self):
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
                if self.mainboard.actionCards[14+boxx*3+boxy].meeple is not None:
                    pygame.draw.circle(self.DISPLAYSURF, self.mainboard.actionCards[14+boxx*3+boxy].meeple, (left+int(BOXSIZE/2),top+int(BOXSIZE*3/4) ), 20, 0)
                if self.mainboard.round <= boxx*3+boxy:
                    break
            else:
                continue
            break
                    #meepleImg = pygame.image.load('Meeple.png').convert_alpha()
                    #meepleImg.fill(mainboard.actionCards[boxx*3+boxy].meeple.playercolor)
                    #DISPLAYSURF.blit(meepleImg, (left+int(BOXSIZE/2), top+int(BOXSIZE/2)))
    def drawfarmyard(self,viewedplayer):
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