'''
Created on 2018/03/07

@author: Yuya
'''
class PlayerBoard:
    def __init__(self,playername='Alex',seatNumber,playercolor=(0,255,0)):
        self.playername = playername
        self.seatNumber = seatNumber
        self.playercolor = playercolor
        self.board =　[[[] for i in range(5)] for j in range(3)]
        self.board[1][0] = self.board[2][0] = 'woodroom'
        self.fences = 15
        self.stables = 4
        self.begging = 0
        self.activeMember = 2
        self.baby = 0
        self.supply = {'wood':0,'clay':0,'reed':0,'stone':0,'food':3,'grain':0,'vegetable':0,'sheep':0,'wild boar':0,'cattle':0}
        if self.seatNumber == 1:
            self.supply['food'] -= 1
        self.handOccup = []
        self.handMinorI = []
        self.openCards = []
    def getGraphic(self):