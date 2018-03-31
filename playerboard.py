'''
Created on 2018/03/07

@author: Yuya
'''
BOARDWIDTH = 5 # number of columns of icons
BOARDHEIGHT = 3 # number of rows of icons
class PlayerBoard:
    def __init__(self,playername='Alex',seatNumber=1,playercolor=(0,255,0)):
        self.playername = playername
        self.seatNumber = seatNumber
        self.playercolor = playercolor
        self.board = [[['_'] for i in range(BOARDHEIGHT)] for j in range(BOARDWIDTH)]
        self.board[1][0] = self.board[2][0] = 'woodroom'
        self.fences = 15
        self.stables = 4
        self.begging = 0
        self.activeMember = 2
        self.workingMember = 0
        self.baby = 0
        self.supply = {'木':0,'煉瓦':0,'葦':0,'石':0,'飯':3,'小麦':0,'野菜':0,'羊':0,'猪':0,'牛':0}
        if self.seatNumber == 1:
            self.supply['飯'] -= 1
        self.handOccup = []
        self.handMinorI = []
        self.openCards = []
    #def drawGraphic(self,pygame,DISPLAYSURF,perspectivePlayer):