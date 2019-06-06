# -*- coding: utf-8 -*-


#######################################準備工作###############################################

# 初始化模組
import pygame
import random
import sys

# 腳色技能dict
characters_dict = {'土木': {'credit': 140, 'attack': 4, 'ActiveAbility': None, 'PassiveAbility': '收回扣', 'definition': '買完土地、或建蓋城堡後，可以回收10%消耗的錢幣'}, \
    '機械': {'credit': 140, 'attack': 4, 'ActiveAbility': '工具人', 'PassiveAbility': None, 'definition': '蓋城堡時可直接升級城堡血量10點'}, \
    '國企': {'credit': 129, 'attack': 4, 'ActiveAbility': 'elite光環', 'PassiveAbility': None, 'definition': '遊戲介面上的角色發出光芒一下下'}, \
        '會計': {'credit': 133, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '四萬保底3萬8', 'definition': '每回合自動獲得2錢幣'}, \
        '經濟': {'credit': 128, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '一隻看不見的手', 'definition': '土地被其他玩家踩到時，可偷取對方10%的錢幣'}, \
            '醫學': {'credit': 229, 'attack': 5, 'ActiveAbility': '妙手回春', 'PassiveAbility': None, 'definition': '在該角色回合開始時，可選擇是否使用妙手回春，選擇任一擁有的一棟建築，回覆該建築物至滿血狀態(每場遊戲只能使用一次)'}}, \
                '哲學': {'credit': 128, 'attack': 3, 'ActiveAbility': '你轉系了嗎', 'PassiveAbility': '我唯一知道的，就是我什麼都不知道', 'definition': '擲骰子的點數翻倍'}, \
                    '中文': {'credit': 128, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '讀書人的事...怎麼能算偷呢', 'definition': '對方玩家經過我土地(含城堡)時，除了收取過路費外，還可以偷取對方1錢幣'}, \
                    '生科': {'credit': 128, 'attack': 2, 'ActiveAbility': None, 'PassiveAbility': '一日生科，終生ㄎㄎ', 'definition': '對方玩家攻擊該玩家的土地或城堡，每次只會受到2點傷害'}, \
                        '法律': {'credit': 130, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '這我一定吉', 'definition': '法律系所持有城堡被打下時，扣除打下者10%的錢幣'}}

class Player():
    def __init__(self, image, name, graduationCredit, attack, ActiveAbility, PassiveAbility, definition):
        self.name = name                    # 角色(科系)
        self.money = 10                     # 星星數
        self.credit = 0                     # 目前學分數
        self.graduationCredit = graduationCredit           # 畢業學分數(取決於角色)
        self.attack = attack                    # 攻擊力(取決於角色)
        self.creditable = True              # 每回合結束可否拿學分
        self.isActive = False               # 是否有主動技能
        self.ActiveAbility = ActiveAbility           # 主動技能名稱
        self.PassiveAbility = PassiveAbility   # 被動技能名稱
        self.isGoingToMove = False 
        self.movable = True                 # 每回合是否可移動
        self.image = image
        self.position = 0  
        self.temp_position = False
        self.dice_value = 0                 # 骰子點數
        self.locatedLand = 0                # 所在位置土地名稱
        self.showText = []                
        self.ownedLands = []                # 總共持有的土地
        self.isShowText = False
        self.definition = definition
        # 每回合一些變數要重新用回初始值，因過程可能改變，像是movable，creditable
    

    def judgePosition(self, lands): # 位置判斷 返回值是玩家所在位置的土地名稱
        for land in lands:
            for position in land.location:
                if self.position == position:
                    return land
                    
            
    def isBuyingLand(self, isPressYes):    # 是否購買土地
        if isPressYes and self.locatedLand.owner == None:
            if self.name == '土木':
                self.locatedLand.owner = self.name
                self.locatedLand.wasBought = True
                self.ownedLands.append(self.locatedLand)
                self.money -= self.locatedLand.price * 0.9
                textline0 = self.name + '購買了' + self.locatedLand.name + '!'
                textline1 = '此角色被動技能為【%s】' % self.PassiveAbility
                textline2 = '買完土地、或建蓋城堡後，可以回收百分之十的消耗錢幣!'
                textline3 = '已回收%d錢幣' % self.locatedLand.price * 0.1
                self.showText = [textline0, textline1, textline2, textline3]
                return True
            else:
                self.locatedLand.owner = self.name
                self.locatedLand.wasBought = True
                self.ownedLands.append(self.locatedLand)
                self.money -= self.locatedLand.price
                self.showText = [self.name + '購買了' + self.locatedLand.name + '!']
                return True
        else:
            return False
        
          
    def isBuildingCastle(self, isPressYes): # 是否在土地上蓋城堡
        try:
            if isPressYes and self.locatedLand.owner == self.name:
                if self.name == '土木': # 土木系技能
                    self.money -= self.locatedLand.price * 0.9
                    textline0 = self.name + '在' + self.locatedLand.name + '建蓋了城堡!' + \
                        '它的過路費是%d' % self.locatedLand.payment
                    textline1 = '此角色被動技能為【%s】' % self.PassiveAbility
                    textline2 = '買完土地、或建蓋城堡後，可以回收百分之十的消耗錢幣!'
                    textline3 = '已回收%d錢幣' % self.locatedLand.price * 0.1
                    self.showText = [textline0, textline1, textline2, textline3]
                    return True

                elif self.name == '機械': # 機械系技能
                    textline0 = self.name + '在' + self.locatedLand.name + '建蓋了城堡!' + \
                        '它的過路費是%d' % self.locatedLand.payment
                    textline1 = '此角色被動技能為【%s】' % self.PassiveAbility
                    textline2 = '建蓋城堡後，城堡升級，血量+10!'
                    self.locatedLand.HP += 10
                    self.showText = [textline0, textline1, textline2]
                    return True
                
                else:
                    self.money -= self.locatedLand.payment
                    self.showText = [self.name + '在' + self.locatedLand.name + '建蓋了城堡！',\
                                '它的過路費是%d' % self.locatedLand.payment]
                    self.soundPlayList = 2
                    self.locatedLand.islocatedCastle = True
                    return True
            else:
                return False
        except:
            pass
    

    def move(self, buildings, allplayers):   # 移動方法 返回值是所在的土地位置
        if self.name == '哲學': # 哲學系技能
            self.dice_value =  random.randint(1,6) * 2
        else:
            self.dice_value =  random.randint(1,6)
        self.position += self.dice_value

        if self.position >= '...': # (...)取決於地圖格數
            self.position -= '...'
        self.locatedLand = self.judgePosition(lands)
        self.isShowText = True
        return self.eventInPosition(allplayers)
    
    
    def isAttacking(self, land, isPressYes):  # 是否要攻打城堡
        if isPressYes:
            if (land.HP > 2) and (land.owner == '生科'): # 生科系技能
                land.HP -= 2
                self.money -= land.payment
                land.owner.money += land.payment
                textline0 = '此角色被動技能為【%s】' % self.PassiveAbility
                textline1 = '別人攻擊該玩家的土地或建築，每次只會受到2點傷害!'
                self.showText = [textline0, textline1]

            elif land.HP > self.attack:
                land.HP -= self.attack
                self.money -= land.payment
                land.owner.money += land.payment

            else:
                if land.owner == '法律': # 法律系技能
                    self.money -= self.money * 0.1
                    land.owner = self.name
                    land.HP = land.temp_HP
                else:
                    land.owner = self.name
                    land.HP = land.temp_HP
        else:
            self.money -= land.payment
            land.owner.money += land.payment


    def eventInPosition(self, allplayers):        # 判斷在土地位置應該發生事件        
        land = self.locatedLand
        if land.name != '機會命運':
            if land.wasBought == False: # 土地未被買時 顯示土地資訊(價格、過路費等等)
                textLine0 = self.name +'骰出了' + '%d' % self.dice_value + '點！'
                textLine1 = self.name +'來到了' + land.name + '!'
                textLine2 = '購買價格：%d' % land.price
                textLine3 = '過路收費：%d' % land.payment
                textLine4 = '是否購買?'
                self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4]
                return True

            elif land.owner == self.name: # 路過自己的土地 蓋城堡
                if land.islocatedCastle == True:
                    '''
                    textline
                    '''
                else:
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了自己的'+ self.locatedLand.name + '!'
                    textLine2 = '可以蓋城堡！' 
                    textLine3 = '加蓋收費：%d' % land.payment
                    textLine4 = '是否加蓋?'
                    self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4]
                    return True

            else:
                component = land.owner # 走到非自己土地上的敵方名字(科系)
                if component == '經濟': # 經濟系技能
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了' + component + '的'+ self.locatedLand.name + '!'
                    textLine2 = '是否要攻打' + component + '的城堡?' 
                    textLine3 = '選擇不攻打會被徵收過路費：%d' % land.payment + '!'
                    textLine4 = '經濟系玩家被動技能為【%s】' % land.owner.PassiveAbility
                    textLine5 = '土地被踩到時，可偷取對方10%的錢幣'
                    textLine6 = '您已被經濟系玩家偷取%d的錢幣' % self.money * 0.1
                    component.money += self.money * 0.1
                    self.money -= self.money * 0.1
                    self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4, textLine5, textLine6]
                    return True

                elif component == '中文':
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了' + component + '的'+ self.locatedLand.name + '!'
                    textLine2 = '是否要攻打' + component + '的城堡?' 
                    textLine3 = '選擇不攻打會被徵收過路費：%d' % land.payment + '!'
                    textLine4 = '中文系玩家被動技能為【%s】' % land.owner.PassiveAbility
                    textLine5 = '經過中文系玩家土地(含城堡)時，除了被收取過路費外，還會被偷取1錢幣'
                    textLine6 = '您已被中文系玩家偷取1錢幣'
                    component.money += 1
                    self.money -= 1
                    self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4, textLine5, textLine6]
                    return True

                else:
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了' + component + '的'+ self.locatedLand.name + '!'
                    textLine2 = '是否要攻打' + component + '的城堡?' 
                    textLine3 = '選擇不攻打會被徵收過路費：%d' % land.payment + '!'
                    self.showText = [textLine0, textLine1, textLine2, textLine3]
                    return 0 # main函數根據0來執行是否攻打城堡

        else: # 骰到機會命運的格子
            whichone = random.randint(0, 6)
            if whichone == 0:
                textLine2 = '機會命運: 這學期被當光'
                textLine3 = '當回合拿不到學分！'
                self.creditable = False

            if whichone == 1:
                if self.money >= 5:
                    textLine2 = '機會命運: 出國進修喝洋墨水'
                    textLine3 = '花費5錢幣，攻擊力上升1點'
                    self.money -= 5
                    self.attack += 1
                else:
                    textLine2 = '機會命運: 出國進修'
                    textLine3 = '花費5錢幣，攻擊力上升1點，但因錢幣不夠，無法獲得此功能'
                    pass

            if whichone == 2:
                textLine2 = '機會命運: 水源阿伯之逆襲'
                textLine3 = '腳踏車被拖吊，下一回合不能行動'
                self.movable = False

            if whichone == 3:
                textLine2 = '機會命運: 抱強者粗大腿'
                textLine3 = '獲得學分最高玩家學分數的20%'
                credits_list = []
                for player in allplayers:
                    credits_list.append(player.credit)
                self.credit += credits_list.max() * 0.2

            if whichone == 4:
                textLine2 = '機會命運: 舟山路大淹水'
                textLine3 = '醫學系以外的玩家因為交通阻塞，下一回合不能行動'
                for player in allplayers:
                    if player.name != '醫學':
                        player.movable = False # 這邊只設定停止一回合

            if whichone == 5:
                textLine2 = '機會命運: 凱道誓師大會'
                textLine3 = '醫學系的玩家因為交通阻塞，下一回合不能行動'
                for player in allplayers:
                    if player.name == '醫學':
                        player.movable = False # 這邊只設定停止一回合

            if whichone == 6:
                if self.money >= 5:
                    textLine2 = '機會命運: 暑修危機分'
                    textLine3 = '花費5錢幣，學分數上升3點'
                    self.money -= 5
                    self.credit += 3
                else:
                    textLine2 = '暑修危機分'
                    textLine3 = '花費5錢幣，學分數上升3點，但因錢幣不夠，無法獲得此功能'
                    pass

            textLine0 = self.name + '骰出了' + '%d' % self.dice_value + '點！'
            textLine1 = '來到了機會命運之地！'
            self.showText = [textLine0, textLine1, textLine2, textLine3]



class Land():                           
    def __init__(self, name, price, payment, location, HP):
        self.name = name                     # 土地名稱
        self.price = price                   # 土地價格
        self.payment = payment               # 土地過路費
        self.location = location             # 土地地圖座標
        self.wasBought = False               # 土地是否被購買
        self.owner = None                    # 土地持有人(科系)
        self.islocatedCastle = False         # 土地是否有蓋城堡
        self.HP = HP                         # 土地血量(會變動)
        self.temp_HP = HP                    # 土地血量(不會變動)，用來重置血量當城堡被打掉時



'''
lands = [] # 地圖土地資訊
'''

'''
醫學系技能
哲學系技能列印文字
生科系技能列印文字
角色主動技能
'''

'''
main function
先判斷當前player是否有主動技能，然後詢問是否要使用
然後要判斷player是否可移動movable = True
每回合要刷新 movable刷新成True要放在會讓玩家下回合不能動的事件指令前但在判斷玩家本回合可不可以動然後擲骰子的指令後
'''

