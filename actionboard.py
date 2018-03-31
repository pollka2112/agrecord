'''
Created on 2018/03/07

@author: Yuya
'''
import random

FPS = 20 # frames per second, the general speed of the program
WINDOWWIDTH = 2048 # size of window's width in pixels
WINDOWHEIGHT = 1536 # size of windows' height in pixels
BOXSIZE = 150 # size of box height & width in pixels
GAPSIZE = 20 # size of gap between boxes in pixels
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
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
LEAFGREEN= (109, 224,  81)
GLINK = (('赤',1,RED),('オスマン',2,BLUE),('ニノ',3,ORANGE),('ぐれそ',4,PURPLE),('シゲヨシ',5,GRAY))

BGCOLOR = LEAFGREEN
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

class ActionCards:
    def __init__(self,spaceName='No Name',accumu={},unaccumu={},actRights=[],stageround=0):
        self.name = spaceName
        self.accumu = accumu
        self.unaccumu = unaccumu
        self.actRights = actRights
        self.goods = {}
        self.meeple = None
        self.stageround = stageround 

    def prepare(self):
        if len(self.accumu.keys()) != 0:
            for item in self.accumu.keys():
                if item in self.goods:
                    self.goods[item] += self.accumu[item]
                else:
                    self.goods[item] = self.accumu[item]
    def doAction(self,player):
        if len(self.goods.keys()) != 0: 
            for item in self.goods.keys():
                player.supply[item] += self.goods[item]
            self.goods.clear()
        if len(self.unaccumu.keys()) != 0:
            for item in self.unaccumu.keys():
                player.supply[item] += self.unaccumu[item]
        if len(self.actRights) != 0:
            player.actRights = self.actRights
    
    def returnHome(self):
        self.meple = None

BrBs = ActionCards('建築 そ/ま 厩',{},{},['Build rooms','Build Stables'])
SPMI = ActionCards('スタピ そ/ま 1小進歩',{},{},['Start Player','MinorI'])
Grain1 = ActionCards('小麦１',{},{'小麦':1},[])
Field1 = ActionCards('畑を耕す',{},{},['Field'])
Occupation1 = ActionCards('職業１',{},{},['1stOccupation'])
DayLaborer = ActionCards('日雇い労働',{},{'飯':2},[])
Wood3 = ActionCards('木３',{'木':3},{},[])
Reed1 = ActionCards('葦１',{'葦':1},{},[])
Clay1 = ActionCards('レンガ１',{'煉瓦':1},{},[])
Fishing = ActionCards('漁１飯',{'飯':1},{},[])
#5人戦
Wood4 = ActionCards('木4',{'木':4},{},[])
Clay3 = ActionCards('レンガ３',{'煉瓦':3},{},[])
RSW = ActionCards('葦石木１',{'葦':1},{'石':1,'木':1},[])
food3Ani = ActionCards('羊１飯１ /豚1 /飯１で牛１',{},{},['Animals'])
Occu_FG = ActionCards('職業１ または 増員',{},{},['Occu_FG'])
#ラウンドカード
Sheep1 = ActionCards('羊１',{'羊':1},{},[],1)
SowBB = ActionCards('種をまく そ/ま パンを焼く',{},{},['Sow','Bake Bread'],1)  
MIMI = ActionCards('小進歩１ または 大進歩１',{},{},['MIMI'],1)
Fences = ActionCards('柵を建てる',{},{},['Fences'],1)
Renovation = ActionCards('建築',{},{},['Renovation'],2)
Stone1W = ActionCards('石1',{'石':1},{},[],2)
FGrowth = ActionCards('増員 そして 小進歩1',{},{},['FGrowth','MinorI'],2)
WildBoar1 = ActionCards('猪１',{'猪':1},{},[],3)
Vegetable1 = ActionCards('野菜１',{},{'野菜':1},[],3)
Cattle1 = ActionCards('牛１',{'牛':1},{},[],4)
Stone1E = ActionCards('石１',{'石':1},{},[],4)
FieldSow = ActionCards('畑を耕す そ/ま 種をまく',{},{},['Field','Sow'],5)
FGwithout = ActionCards('部屋無し 増員',{},{},['FGwithout'],5)
RenoFence = ActionCards('改築 そして 柵',{},{},['Renovation','Fences'],6)

FIRSTSTAGE = [Sheep1,SowBB,MIMI,Fences]
SECONDSTAGE = [Renovation,Stone1W,FGrowth]
THIRDSTAGE = [WildBoar1,Vegetable1]
FOURTHSTAGE = [Cattle1,Stone1E]
FIFTHSTAGE = [FieldSow,FGwithout]
SIXSTAGE = [RenoFence]
STAGECARDS = [FIRSTSTAGE,SECONDSTAGE,THIRDSTAGE,FOURTHSTAGE,FIFTHSTAGE,SIXSTAGE]

class Actionboard:
    def __init__(self):
        self.round = 0
        self.phase = '準備フェイズ'#'労働フェイズ','帰宅フェイズ','畑フェイズ','食料供給フェイズ','繁殖フェイズ')
        self.actionCards = [BrBs,SPMI,Grain1,Field1,Occupation1,DayLaborer, Wood3,Reed1,Clay1,Fishing]
        self.actionCards.extend([Wood4,Clay3,RSW,food3Ani,Occu_FG])
        for stage in STAGECARDS:
            random.shuffle(stage)
            self.actionCards.extend(stage)
        self.actionRect = []
        self.playerCirc = []
        self.pagecTri = []