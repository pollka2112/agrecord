'''
Created on 2018/03/07

@author: Yuya
'''
import random
class Actionboard:
    def __init__(self):
        self.round = 0
        self.phase = ('Preparation Phase','Work Phase','Returning Home Phase','Field Phase','Feeding Phase','Breeding Phase')
        self.actionCards = [BrBs,SPMI,Grain1,Field1,Occupation1,DayLaborer, Wood3,Reed1,Clay1,Fishing]
        self.actionCards.extend([Wood4,Clay3,RSW,food3Ani,Occu_FG])
        self.actionCards.extend(random.shuffle([Sheep1,SowBB,MIMI,Fences]))
        self.actionCards.extend(random.shuffle([Renovation,Stone1W,FGrowth]))
        self.actionCards.extend(random.shuffle([WildBoar1,Vegetable1]))
        self.actionCards.extend(random.shuffle([Cattle1,Stone1E]))
        self.actionCards.extend(random.shuffle([FieldSow,FGwithout]))
        self.actionCards.append(RenoFence)
    
    def getGraphic(self):
        
class ActionCards:
    def __init__(self,spaceName='No Name',accumu={},unaccumu={},actRights=[],stageround):
        self.name = spaceName
        self.accumu = accumu
        self.unaccumu = unaccumu
        self.actRights = actRights
        self.goods = {}
        self.meple = None
        self.stageround = stageround 

    def prepare(self):
        if len(self.accumu.keys()) != 0:
            for item in self.accumu.keys():
                self.goods[item] += self.accumu[item]
    
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
BrBs = ActionCards('建築　そして/または 厩を建てる',{},{},['Build rooms','Build Stables'],0)
SPMI = ActionCards('スタートプレイヤー　そして/または 1小進歩',{},{},['Start Player','MinorI'],0)
Grain1 = ActionCards('小麦１',{},{'grain':1},[],0)
Field1 = ActionCards('畑を耕す',{},{},['Field'],0)
Occupation1 = ActionCards('職業１',{},{},['1stOccupation'],0)
DayLaborer = ActionCards('日雇い労働',{},{'food':2},[],0)
Wood3 = ActionCards('木３',{'wood':3},{},[],0)
Reed1 = ActionCards('葦１',{'reed':1},{},[],0)
Clay1 = ActionCards('レンガ１',{'clay':1},{},[],0)
Fishing = ActionCards('漁１飯',{'food':1},{},[],0)
#5人戦
Wood4 = ActionCards('木4',{'wood':4},{},[],0)
Clay3 = ActionCards('レンガ３',{'clay':3},{},[],0)
RSW = ActionCards('葦石木１',{'reed':1},{'stone':1,'wood':1},[],0)
food3Ani = ActionCards('羊１飯１/豚1/飯１で牛１',{},{},['Animals'],0)
Occu_FG = ActionCards('職業１　または　家族を増やす',{},{},['Occu_FG'],0)
#ラウンドカード
Sheep1 = ActionCards('羊１',{'sheep':1},{},[],1)
SowBB = ActionCards('種をまく　そして/または　パンを焼く',{},{},['Sow','Bake Bread'],1)  
MIMI = ActionCards('小進歩１　または　大進歩１',{},{},['MIMI'],1)
Fences = ActionCards('柵を建てる',{},{},['Fences'],1)
Renovation = ActionCards('建築',{},{},['Renovation'],2)
Stone1W = ActionCards('石1',{'stone':1},{},[],2)
FGrowth = ActionCards('家族を増やす　そして　小進歩1',{},{},['FGrowth','MinorI'],2)
WildBoar1 = ActionCards('猪１',{'wild boar':1},{},[],3)
Vegetable1 = ActionCards('野菜１',{},{'vegetable':1},[],3)
Cattle1 = ActionCards('牛１',{'cattle':1},{},[],4)
Stone1E = ActionCards('石１',{'stone':1},{},[],4)
FieldSow = ActionCards('畑を耕す　そして/または 種をまく',{},{},['Field','Sow'],5)
FGwithout = ActionCards('部屋が無くても家族を増やす',{},{},['FGwithout'],5)
RenoFence = ActionCards('改築　そして　柵を建てる',{},{},['Renovation','Fences'],6)