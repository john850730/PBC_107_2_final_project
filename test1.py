# -*- coding: utf-8 -*-


#######################################準備工作###############################################

# 初始化模組
import pygame
import random
import sys

# 角色資訊(dictionary)
characters_dict = \
   {'土木': {'credit': 140, 'attack': 4, 'ActiveAbility': None, 'PassiveAbility': '收回扣', 'definition': '買完土地、或建蓋城堡後，可以回收10%消耗的錢幣'}, \
    '機械': {'credit': 140, 'attack': 4, 'ActiveAbility': '工具人', 'PassiveAbility': None, 'definition': '蓋城堡時可直接升級城堡血量10點'}, \
    '國企': {'credit': 129, 'attack': 4, 'ActiveAbility': 'elite光環', 'PassiveAbility': None, 'definition': '遊戲介面上的角色發出光芒一下下'}, \
    '會計': {'credit': 133, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '四萬保底3萬8', 'definition': '每回合自動獲得2錢幣'}, \
    '經濟': {'credit': 128, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '一隻看不見的手', 'definition': '土地被其他玩家踩到時，可偷取對方10%的錢幣'}, \
    '醫學': {'credit': 229, 'attack': 5, 'ActiveAbility': '妙手回春', 'PassiveAbility': None, 'definition': '在該角色回合開始時，可選擇是否使用妙手回春，選擇任一擁有的一棟建築，回覆該建築物至滿血狀態(每場遊戲只能使用一次)'}, \
    '哲學': {'credit': 128, 'attack': 3, 'ActiveAbility': '你轉系了嗎', 'PassiveAbility': '我唯一知道的，就是我什麼都不知道', 'definition': '擲骰子的點數翻倍'}, \
    '中文': {'credit': 128, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '讀書人的事...怎麼能算偷呢', 'definition': '對方玩家經過我土地(含城堡)時，除了收取過路費外，還可以偷取對方1錢幣'}, \
    '生科': {'credit': 128, 'attack': 2, 'ActiveAbility': None, 'PassiveAbility': '一日生科，終生ㄎㄎ', 'definition': '對方玩家攻擊該玩家的土地或城堡，每次只會受到2點傷害'}, \
    '法律': {'credit': 130, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '這我一定吉', 'definition': '法律系所持有城堡被打下時，扣除打下者10%的錢幣'}}

# 角色物件
class Player():
    def __init__(self, image, name, graduationCredit, attack, ActiveAbility, PassiveAbility, definition):
        self.image = image                             # 角色圖片
        self.name = name                               # 角色(科系)
        self.money = 10                                # 星星數
        self.credit = 0                                # 目前學分數
        self.graduationCredit = graduationCredit       # 畢業學分數(取決於角色)
        self.attack = attack                           # 攻擊力(取決於角色)
        self.creditable = True                         # 每回合結束可否拿學分
        self.getcredit = 0                             # 每回合可獲得的學分數
        self.getmoney = 0                              # 每回合可獲得的錢幣
        self.isActive = False                          # 是否有主動技能
        self.ActiveAbility = ActiveAbility             # 主動技能名稱
        self.PassiveAbility = PassiveAbility           # 被動技能名稱
        self.isGoingToMove = False 
        self.movable = True                            # 每回合是否可移動
        self.position = 0                              # 每回合骰完骰子，要到達的位置
        self.temp_position = False
        self.dice_value = 0                            # 骰子點數
        self.locatedLand = 0                           # 所在位置土地名稱
        self.showText = []                             # 要印出的文字
        self.ownedLands = []                           # 總共持有的土地
        self.isShowText = False
        self.definition = definition
		
        # 每回合一些變數要重新用回初始值，因過程可能改變，像是movable，creditable
    

    def judgePosition(self, lands): # 位置判斷，返回值是玩家所在位置的土地名稱
        for land in lands:
            for position in land.location:
                if self.position == position:
                    return land
                    
            
    def isBuyingLand(self, isPressYes):    # 是否購買土地，isPressYes = True 代表玩家已經決定要買土地
        if isPressYes and self.locatedLand.owner == None:
            if self.name == '土木': # 土木系技能
                self.locatedLand.owner = self.name
                self.locatedLand.wasBought = True
                self.ownedLands.append(self.locatedLand)
                self.money -= self.locatedLand.price * 0.9
                textline0 = self.name + '購買了' + self.locatedLand.name + '!'
                textline1 = '此角色被動技能為【%s】' % self.PassiveAbility
                textline2 = '買完土地、或建蓋城堡後，可以回收百分之十的消耗錢幣!'
                textline3 = '已回收%d錢幣' % self.locatedLand.price * 0.1
                self.showText = [textline0, textline1, textline2, textline3]
                self.isShowText = True
                return True
            else:
                self.locatedLand.owner = self.name
                self.locatedLand.wasBought = True
                self.ownedLands.append(self.locatedLand)
                self.money -= self.locatedLand.price
                self.showText = [self.name + '購買了' + self.locatedLand.name + '!']
                self.isShowText = True
                return True
        else:
            return False
        
          
    def isBuildingCastle(self, isPressYes): # 是否在土地上蓋城堡，isPressYes = True 代表玩家已經決定要蓋城堡
        try:
            if isPressYes and self.locatedLand.owner == self.name:
                if self.name == '土木': # 土木系技能
                    self.locatedLand.islocatedCastle = True
                    self.money -= self.locatedLand.price * 0.9
                    textline0 = self.name + '在' + self.locatedLand.name + '建蓋了城堡!' + \
                        '它的過路費是%d' % self.locatedLand.payment
                    textline1 = '此角色被動技能為【%s】' % self.PassiveAbility
                    textline2 = '買完土地、或建蓋城堡後，可以回收百分之十的消耗錢幣!'
                    textline3 = '已回收%d錢幣' % self.locatedLand.price * 0.1
                    self.showText = [textline0, textline1, textline2, textline3]
                    self.isShowText = True
                    return True

                elif self.name == '機械': # 機械系技能
                    self.locatedLand.islocatedCastle = True
                    self.money -= self.locatedLand.price
                    textline0 = self.name + '在' + self.locatedLand.name + '建蓋了城堡!' + \
                        '它的過路費是%d' % self.locatedLand.payment
                    textline1 = '此角色被動技能為【%s】' % self.PassiveAbility
                    textline2 = '建蓋城堡後，城堡升級，血量+10!'
                    self.locatedLand.HP += 10
                    self.showText = [textline0, textline1, textline2]
                    self.isShowText = True
                    return True
                
                else:
                    self.locatedLand.islocatedCastle = True
                    self.money -= self.locatedLand.price
                    self.showText = [self.name + '在' + self.locatedLand.name + '建蓋了城堡！',\
                                '它的過路費是%d' % self.locatedLand.payment]
                    self.isShowText = True
                    return True
            else:
                return False
        except:
            pass
    

    def move(self, buildings, allplayers):   # 移動方法 返回值是所在的土地位置
        if self.name == '哲學': # 哲學系技能
            self.dice_value =  random.randint(1,6) * 2
            self.position += self.dice_value
            textline0 = '此角色被動技能為【%s】' % self.PassiveAbility
            textline1 = '擲骰子點數翻倍!'
            self.showText = [textline0, textline1]
            self.isShowText = True
        else:
            self.dice_value =  random.randint(1,6)
            self.position += self.dice_value

        if self.position >= 24: # 地圖有24格
            self.position -= 24
        self.locatedLand = self.judgePosition(lands)
        return self.eventInPosition(allplayers) # 玩家當前位置會發生的事件
    
    
    def isAttacking(self, land, isPressYes):  # 是否要攻打城堡，isPressYes = True 代表玩家已經決定攻打城堡
        if isPressYes and land.owner != self.name:
            if (land.HP > 2) and (land.owner == '生科'): # 生科系技能
                land.HP -= 2
                self.money -= land.payment
                land.owner.money += land.payment
                textline0 = '此城堡持有者為【%s】' % land.owner
                textline1 = '此城堡持有者的被動技能為【%s】' % land.owner.PassiveAbility
                textline2 = '別人攻擊該玩家的土地或建築，每次只會受到2點傷害!'
                self.showText = [textline0, textline1, textline2]
                self.isShowText = True

            elif land.HP > self.attack:
                land.HP -= self.attack
                self.money -= land.payment
                land.owner.money += land.payment
                textline0 = '此城堡持有者為【%s】' % land.owner
                textline1 = '您已造成此城堡血量降低%d' % self.attack
                textline2 = '可惜沒攻打下來，您已被收取%d錢幣的過路費' % land.payment
                self.showText = [textline0, textline1, textline2]
                self.isShowText = True

            else:
                if land.owner == '法律': # 法律系技能
                    self.money -= self.money * 0.1
                    land.owner = self.name
                    land.HP = land.temp_HP
                    textline0 = '此城堡持有者為【%s】' % land.owner
                    textline1 = '此城堡持有者的被動技能為【%s】' % land.owner.PassiveAbility
                    textline2 = '城堡被打下時，扣除打下者10%的錢幣'
                    textline3 = '恭喜!您已成功攻打下這座城堡，現在這座城堡已經屬於您的了!'
                    self.showText = [textline0, textline1, textline2, textline3]
                    self.isShowText = True
                else:
                    land.owner = self.name
                    land.HP = land.temp_HP
                    textline0 = '此城堡持有者為【%s】' % land.owner
                    textline1 = '恭喜!您已成功攻打下這座城堡，現在這座城堡已經屬於您的了!'
                    self.showText = [textline0, textline1]
                    self.isShowText = True
        else:
            self.money -= land.payment
            land.owner.money += land.payment
            textline0 = '此城堡持有者為【%s】' % land.owner
            textline1 = '您已選擇不攻打此座城堡'
            textline2 = '您已被收取%d錢幣的過路費' % land.payment
            self.showText = [textline0, textline1, textline2]
            self.isShowText = True


    def eventInPosition(self, allplayers):  # 判斷角色在土地位置應該發生的事件        
        land = self.locatedLand
        if land.name == '機會命運': # 機會命運的格子
            whichone = random.randint(0, 6)
            if whichone == 0:
                textLine2 = '機會命運: 這學期被當光'
                textLine3 = '當回合拿不到學分！'
                self.creditable = False

            elif whichone == 1:
                if self.money >= 5:
                    textLine2 = '機會命運: 出國進修喝洋墨水'
                    textLine3 = '花費5錢幣，攻擊力上升1點'
                    self.money -= 5
                    self.attack += 1
                else:
                    textLine2 = '機會命運: 出國進修'
                    textLine3 = '花費5錢幣，攻擊力上升1點，但因錢幣不夠，無法獲得此功能'
                    pass

            elif whichone == 2:
                textLine2 = '機會命運: 水源阿伯之逆襲'
                textLine3 = '腳踏車被拖吊，下一回合不能行動'
                self.movable = False

            elif whichone == 3:
                textLine2 = '機會命運: 抱強者粗大腿'
                textLine3 = '獲得學分最高玩家學分數的20%'
                credits_list = []
                for player in allplayers:
                    credits_list.append(player.credit)
                self.credit += credits_list.max() * 0.2

            elif whichone == 4:
                textLine2 = '機會命運: 舟山路大淹水'
                textLine3 = '醫學系以外的玩家因為交通阻塞，下一回合不能行動'
                for player in allplayers:
                    if player.name != '醫學':
                        player.movable = False # 這邊只設定停止一回合

            elif whichone == 5:
                textLine2 = '機會命運: 凱道誓師大會'
                textLine3 = '醫學系的玩家因為交通阻塞，下一回合不能行動'
                for player in allplayers:
                    if player.name == '醫學':
                        player.movable = False # 這邊只設定停止一回合

            else:
                if self.money >= 5:
                    textLine2 = '機會命運: 暑修危機分'
                    textLine3 = '花費5錢幣，學分數上升3點'
                    self.money -= 5
                    self.credit += 3
                else:
                    textLine2 = '暑修危機分'
                    textLine3 = '花費5錢幣，學分數上升3點，但因錢幣不夠，無法獲得此功能'
                    pass

            textLine0 = self.name + '骰出了' + '%d' % self.dice_value + '點!'
            textLine1 = '來到了機會命運之地！'
            self.showText = [textLine0, textLine1, textLine2, textLine3]
            self.isShowText = True

        elif land.name == "送到城中校區":
            textLine0 = '搭錯公車，前往城中校區!'
            textLine1 = '下一回合不能行動'
            self.movable  = False # 不能動一回合
            self.showText = [textLine0, textLine1]
            self.isShowText = True

        elif land.name == '女九自助餐':
            textLine0 = '交到女友，攻擊力加1，但被朋友唾棄，下一回合不能行動'
            self.movable = False
            self.attack += 1
            self.showText = [textLine0]
            self.isShowText = True

        elif land.name == '森林系館':
            textLine0 = '加簽到森多概，交到女友，攻擊力加1，但被朋友唾棄，下一回合不能行動'
            self.movable = False
            self.attack += 1
            self.showText = [textLine0]
            self.isShowText = True
            
        else: # 走到不是你的土地，也不是機會命運地
            if land.wasBought == False: # 土地未被買時 顯示土地資訊(價格、過路費等等)
                textLine0 = self.name +'骰出了' + '%d' % self.dice_value + '點！'
                textLine1 = self.name +'來到了' + land.name + '!'
                textLine2 = '購買價格：%d' % land.price
                textLine3 = '過路收費：%d' % land.payment
                textLine4 = '是否購買?'
                self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4]
                self.isShowText = True
                return True

            elif land.owner == self.name: # 路過自己的土地 蓋城堡
                if land.islocatedCastle == True: # 已經蓋了，不能做事了!
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了自己的城堡!'
                    textLine2 = '美好的一天又過去了！' 
                    self.showText = [textLine0, textLine1, textLine2]
                    self.isShowText = True
                else:
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了自己的'+ self.locatedLand.name + '!'
                    textLine2 = '可以蓋城堡！' 
                    textLine3 = '加蓋收費：%d' % land.payment
                    textLine4 = '是否加蓋?'
                    self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4]
                    self.isShowText = True
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
                    self.isShowText = True
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
                    self.isShowText = True
                    return True

                else:
                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                    textLine1 = '來到了' + component + '的'+ self.locatedLand.name + '!'
                    textLine2 = '是否要攻打' + component + '的城堡?' 
                    textLine3 = '選擇不攻打會被徵收過路費：%d' % land.payment + '!'
                    self.showText = [textLine0, textLine1, textLine2, textLine3]
                    self.isShowText = True
                    return True


class Land():                           
    def __init__(self, name, price, payment, location, HP, creditLv):
        self.name = name                     # 土地名稱
        self.price = price                   # 土地價格
        self.payment = payment               # 土地過路費
        self.location = location             # 土地地圖座標
        self.wasBought = False               # 土地是否被購買
        self.owner = None                    # 土地持有人(科系)
        self.islocatedCastle = False         # 土地是否有蓋城堡
        self.HP = HP                         # 土地血量(會變動)
        self.temp_HP = HP                    # 土地血量(不會變動)，用來重置血量當城堡被打掉時
        self.credit = creditLv               # 土地給的學分等級



# 讓東西透明度可以調整，網路上的
def blit_alpha(target, source, location, opacity):#source一定要是個圖檔!!不可以是按鍵!
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target , (-x , -y))
    temp.blit(source, (0,0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

# 印訊息函數
def printText(player):
    if player.isShowText == True:
        for each in player.showText:
                text = font.render(each, True, white, textColorInMessageBox)
                screen.blit(text, textPosition)
                textPosition[1] += 30


########################################主函數###############################################    


def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # 初始化
    size = (1270,768)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('臺大戰系比武大會')
    
    # 讀取顏色
    textColorInMessageBox = (141,146,152)
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    font = pygame.font.Font('resource\\font\\myfont.ttf',30)
    
    
    # 上傳圖片
    # 基本
    backgroud = pygame.image.load("resource\\pic\\GameMap.png")
    backgroud = pygame.transform.scale(backgroud, (1270,768))
    character_selection = pygame.image.load("resource\\pic\\Charater_selection.png")
    character_selection = pygame.transform.scale(character_selection, (1270,768))
    chess_0 = pygame.image.load("resource\\pic\\chess_0.png")
    chess_1 = pygame.image.load("resource\\pic\\chess_1.png")
    chess_2 = pygame.image.load("resource\\pic\\chess_2.png")
    chess_3 = pygame.image.load("resource\\pic\\chess_3.png")
    chess_4 = pygame.image.load("resource\\pic\\chess_4.png")
    chess_list = [chess_0,chess_1,chess_2,chess_3,chess_4]
    bigdice_image = pygame.image.load("resource\\pic\\dice.png").convert_alpha()
    bigdice_image = pygame.transform.scale(bigdice_image, (150,150))
    dice_1 = pygame.image.load("resource\\pic\\dice_1.png")
    dice_2 = pygame.image.load("resource\\pic\\dice_2.png")
    dice_3 = pygame.image.load("resource\\pic\\dice_3.png")
    dice_4 = pygame.image.load("resource\\pic\\dice_4.png")
    dice_5 = pygame.image.load("resource\\pic\\dice_5.png")
    dice_6 = pygame.image.load("resource\\pic\\dice_6.png")
    dices = [dice_1,dice_2,dice_3,dice_4,dice_5,dice_6]
    yes = pygame.image.load("resource\\pic\\yes.png")
    yes2 = pygame.image.load("resource\\pic\\yes2.png")
    no = pygame.image.load("resource\\pic\\no.png")
    no2 = pygame.image.load("resource\\pic\\no2.png")
    GameStart = pygame.image.load("resource\\pic\\GameStart.png")
    GameStart = pygame.transform.scale(GameStart, (1270,768))
    StartGameButton = pygame.image.load("resource\\pic\\StartGameButton.png").convert_alpha()
    StartGameButton = pygame.transform.scale(StartGameButton, (600,125))
    turnover = pygame.image.load("resource\\pic\\turnover.png")
    turnover2 = pygame.image.load("resource\\pic\\turnover2.png")
    
    #玩家圖檔Image TBD
    imagePlayer0 = pygame.image.load("resource\\pic\\civil_engineering.png").convert_alpha()
    imagePlayer0 = pygame.transform.scale(imagePlayer0, (250,250))
    imagePlayer1 = pygame.image.load("resource\\pic\\machanical_engineering.png").convert_alpha()
    imagePlayer1 = pygame.transform.scale(imagePlayer1, (250,250))
    imagePlayer2 = pygame.image.load("resource\\pic\\elite.png").convert_alpha()
    imagePlayer2 = pygame.transform.scale(imagePlayer2, (250,250))
    imagePlayer3 = pygame.image.load("resource\\pic\\accounting.png").convert_alpha()
    imagePlayer3 = pygame.transform.scale(imagePlayer3, (250,250))
    imagePlayer4 = pygame.image.load("resource\\pic\\econ.png").convert_alpha()
    imagePlayer4 = pygame.transform.scale(imagePlayer4, (250,250))
    imagePlayer5 = pygame.image.load("resource\\pic\\medic.png").convert_alpha()
    imagePlayer5 = pygame.transform.scale(imagePlayer5, (250,250))
    imagePlayer6 = pygame.image.load("resource\\pic\\philosophy.png").convert_alpha()
    imagePlayer6 = pygame.transform.scale(imagePlayer6, (250,250))
    imagePlayer7 = pygame.image.load("resource\\pic\\chinese.png").convert_alpha()
    imagePlayer7 = pygame.transform.scale(imagePlayer7, (250,250))
    imagePlayer8 = pygame.image.load("resource\\pic\\bio_science.png").convert_alpha()
    imagePlayer8 = pygame.transform.scale(imagePlayer8, (250,250))
    imagePlayer9 = pygame.image.load("resource\\pic\\law.png").convert_alpha()
    imagePlayer9 = pygame.transform.scale(imagePlayer9, (250,250))
    
    
    imagePlayers = {"土木":imagePlayer0, "機械":imagePlayer1, "國企":imagePlayer2, '會計':imagePlayer3, '經濟':imagePlayer4\
		   ,'醫學':imagePlayer5, '哲學':imagePlayer6, '中文':imagePlayer7, '生科':imagePlayer8, '法律':imagePlayer9}#dictionary of images of players, keys = "name"

    
    # 各种Surface的rect 
    bigdice_rect = bigdice_image.get_rect()
    bigdice_rect.left , bigdice_rect.top = 50 , 600
    yes_rect = yes.get_rect()
    yes_rect.left , yes_rect.top = 500,438 
    no_rect = no.get_rect()
    no_rect.left , no_rect.top =  630,438
    button_rect = StartGameButton.get_rect()
    button_rect.left , button_rect.top = 500,30
    turnover_rect = turnover.get_rect()
    turnover_rect.left , turnover_rect.top = 1035,613
    ce_rect = imagePlayers['土木'].get_rect()
    ce_rect.left , ce_rect.top = 292,150
    me_rect = imagePlayers['機械'].get_rect()
    me_rect.left , me_rect.top = 42,150
    ib_rect = imagePlayers['國企'].get_rect()
    ib_rect.left , ib_rect.top = 542,150
    acct_rect = imagePlayers['會計'].get_rect()
    acct_rect.left , acct_rect.top = 792,150
    econ_rect = imagePlayers['經濟'].get_rect()
    econ_rect.left , econ_rect.top = 1037,150
    med_rect = imagePlayers['醫學'].get_rect()
    med_rect.left , med_rect.top = 42,420
    phy_rect = imagePlayers['哲學'].get_rect()
    phy_rect.left , phy_rect.top = 292,420
    chi_rect = imagePlayers['中文'].get_rect()
    chi_rect.left , chi_rect.top = 542,420
    bio_rect = imagePlayers['生科'].get_rect()
    bio_rect.left , bio_rect.top = 792,420
    law_rect = imagePlayers['法律'].get_rect()
    law_rect.left , law_rect.top = 1037,420
	
    


    # 創造地方:  name, price, payment, location, HP, creditLv
    gate_Land = Land('大門',0,0,[0],0," ") # 沒事
    philo_Land = Land('哲學系館',2,2,[1],3,"low")
    oppChance1 = Land('機會命運',0,0,[2],0,0)
    lita_Land = Land('文學院',2,2,[3],3,"low")
    civ_Land = Land('土木系館',4,3,[4],5,"mid")
    fore_Land = Land('森林系館',0,0,0,[5]," ") # 停一回合
    engn_Land = Land('工綜',4,3,[6],5,"mid")
    social_Land = Land('社科院',2,4,[7],7,"high")
    law_Land = Land('霖澤館',4,3,[8],5,"mid")
    oppChance2 = Land('機會命運',0,0,[9],0,0)
    hwoDa_Land = Land('活大',6,2,[10],3,"low")
    library_Land = Land('總圖',6,4,[11],7,"high")
    sea_Land = Land('工科海',4,3,[12],5,"mid")
    mDorm_Land = Land('男一舍',2,2,[13],3,"low")
    oppChance3 = Land('機會命運',0,0,[14],0,0)
    fDorm_Land = Land('女九自助餐',0,0,0,[15]," ") # 停一回合
    geo_Land = Land("地理系館",6,2,[16],3,"low")
    biosci_Land = Land("生科館",6,2,[17],3,"low")
    mgmt2_Land = Land('管二',6,4,[18],7,"high")
    mgmt1_Land = Land('管一',6,4,[19],7,"high")
    admin_Land = Land('行政大樓',4,3,[20],5,"mid")
    oppChance4 = Land('機會命運',0,0,[21],0,0)
    watermkt_Land = Land('水源市場',6,2,[22],3,"low")
    chengzhon_Land = Land('送往城中校區',0,0,[23],0," ") # 暫停一回合
	
	
    
    buildings = [gate_Land,philo_Land,oppChance1,lita_Land,civ_Land,\
                 fore_Land,engn_Land,social_Land,law_Land,oppChance2,hwoDa_Land,\
                 library_Land, sea_Land, mDorm_Land, oppChance3, fDorm_Land, geo_Land,\
                 biosci_Land, mgmt2_Land, mgmt1_Land, admin_Land, oppChance4,\
                 watermkt_Land, chengzhon_Land]
    
    majorlist = ['土木', '機械', '國企', '會計', '經濟', '醫學', '哲學', '中文', '生科' ,'法律']
	
    
    '''
    # 座標數據等一下要改
    MapXYvalue = [(435.5,231.5),(509.5,231.5),(588.5,231.5),(675.5,231.5),(758.5,231.5),\
                  (758.5,317.0),(758.5,405.5),(758.5,484.5),(758.5,558.5),(679.5,558.5),\
                  (601.5,558.5),(518.5,556.5),(435.5,556.5),(435.5,479.5),(435.5,399.0),\
                  (435.5,315.5)
                  ]
    
    MapChessPosition_Player = []
    MapChessPosition_Com = []
    MapChessPosition_Original = []
    MapChessPosition_Payment = []
    '''
    
    MapMessageBoxPosition = (474.1 , 276.9)
    YesNoMessageBoxPosition = [(500,438) , (630,438)]
    StartGameButtonPosition = (370,65)
    TurnOvwrButtonPosition = (1035,613)
    
    '''
    # 調整位置
    for i in range(0,24):
        MapChessPosition_Original.append((MapXYvalue[i][0]-50,MapXYvalue[i][1]-80))
        MapChessPosition_Player.append((MapXYvalue[i][0]-70,MapXYvalue[i][1]-60))
        MapChessPosition_Com.append((MapXYvalue[i][0]-30,MapXYvalue[i][1]-100))
        MapChessPosition_Payment.append((MapXYvalue[i][0]-30,MapXYvalue[i][1]-15))
    '''
    
    
        
    
    # 循環用      
    running = True
    image_alpha = 255
    button_alpha = 255
    half_alpha = 30
    showdice = True
    showYes2 = False
    showNo2 = False
    showYes_No = False
    pressYes = False
    whetherYes_NoJudge = False
    gameStarted = False
    selectCharacter = False
    showButton2 = False
    selected = []                        # 已選取的角色
    Medic_Skills_counter = 0             # 判斷醫學系技能剩下次數
    Medic_harmed_buildings = []		     # 判斷醫學系受損建築

    
    # 播放背景音樂(暫無)
    # pygame.mixer.music.play(100)


########################################遊戲循環開始###############################################    


   # 循環開始！ 
    while running:



        if not gameStarted:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
				
                if event.type == pygame.MOUSEMOTION:#如果滑鼠有晃到
                    if button_rect.collidepoint(event.pos):#這一個矩形內
                        button_alpha = 255#變暗   
                    else:
                        button_alpha = 120#變亮 

                if event.type == pygame.MOUSEBUTTONDOWN:#如果有暗下按鈕
                    if button_rect.collidepoint(event.pos): # 且是點在個矩形內                    
                        selectCharacter = True#始可已進入下一個if selectCharacter block
                        gameStarted = True#不再進入if not gameStarted的block
            screen.blit(GameStart, (0,0))#印出底圖一       
            blit_alpha(screen, StartGameButton, StartGameButtonPosition, button_alpha)#放上start game按鍵，且會改變亮度!
			
		# 進入選角頁面	
        if selectCharacter:
            # 選角介面設定
            screen.blit(character_selection, (0,0))#放上選角底圖 
            #原本按鈕是比較淺色的，希望按鈕點完後變暗(變255)
            blit_alpha(screen, imagePlayers['機械'], (42, 150), 180)
            blit_alpha(screen, imagePlayers['土木'], (292, 150), 180)
            blit_alpha(screen, imagePlayers['國企'], (542, 150), 180)
            blit_alpha(screen, imagePlayers['會計'], (792, 150), 180)
            blit_alpha(screen, imagePlayers['經濟'], (1037, 150),180)
            blit_alpha(screen, imagePlayers['醫學'], (42, 420), 180)
            blit_alpha(screen, imagePlayers['哲學'], (292, 420), 180)
            blit_alpha(screen, imagePlayers['中文'], (542, 420), 180)
            blit_alpha(screen, imagePlayers['生科'], (792, 420), 180)
            blit_alpha(screen, imagePlayers['法律'], (1037, 420), 180)
            pygame.display.flip()
            clock.tick(60)
            
			#選角色(四個)
            allset = 0
            selected = []
            while allset < 4:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ce_rect.collidepoint(event.pos):
							blit_alpha(screen, imagePlayers['土木'], (292, 150), 255)#如果點了，就會blit一個比較深色的按扭圖按上去                    
                            selected.append('土木')
                            allset += 1
                        if me_rect.collidepoint(event.pos):
							blit_alpha(screen, imagePlayers['機械'], (42, 150), 255)
                            selected.append('機械')
                            allset += 1
                        if ib_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['國企'], (542, 150), 255)                           
                            selected.append('國企')
                            allset += 1
                        if acct_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['會計'], (792, 150), 255)                           
                            selected.append('會計')
                            allset += 1
                        if econ_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['經濟'], (1037, 150),255)                           
                            selected.append('經濟')
                            allset += 1
                        if med_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['醫學'], (42, 420), 255)                         
                            selected.append('醫學')
                            allset += 1
                        if phy_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['哲學'], (292, 420), 255)                          
                            selected.append('哲學')
                            allset += 1
                        if chi_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['中文'], (542, 420), 255)                           
                            selected.append('中文')
                            allset += 1
                        if bio_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['生科'], (792, 420), 255)                           
                            selected.append('生科')
                            allset += 1
                        if law_rect.collidepoint(event.pos):
                            blit_alpha(screen, imagePlayers['法律'], (1037, 420), 255)                            
                            selected.append('法律')
                            allset += 1


			# 選好角色	
            name1 = selected[0]
            name2 = selected[1]
            name3 = selected[2]
            name4 = selected[3]
            # 創造玩家
            allplayers = [] # 共四個角色

            player1 = Player(imagePlayers[name1], name1, characters_dict[name1]["credit"], characters_dict[name1]["attack"]\
		    ,characters_dict[name1]["ActiveAbility"], characters_dict[name1]["PassiveAbility"], characters_dict[name1]["definition"])
            allplayers.append(player1)

            player2 = Player(imagePlayers[name2], name2, characters_dict[name2]["credit"], characters_dict[name2]["attack"]\
		    ,characters_dict[name2]["ActiveAbility"], characters_dict[name2]["PassiveAbility"], characters_dict[name1]["definition"])
            allplayers.append(player2)

            player3 = Player(imagePlayers[name3], name3, characters_dict[name3]["credit"], characters_dict[name3]["attack"]\
		    ,characters_dict[name3]["ActiveAbility"], characters_dict[name3]["PassiveAbility"], characters_dict[name1]["definition"])
            allplayers.append(player3)

            player4 = Player(imagePlayers[name4], name4, characters_dict[name4]["credit"], characters_dict[name4]["attack"]\
		    ,characters_dict[name4]["ActiveAbility"], characters_dict[name4]["PassiveAbility"], characters_dict[name1]["definition"])
            allplayers.append(player4)

            presentPlayer = player1 # 由player1開始

            selectCharacter = False #不會再進入這一個if block
            
                		
        if gameStarted and allset == 4: # 角色選好後，會變成true，遊戲開始
            # 公佈欄
            M_1 = font.render(player1.name +'Money：%d' % player1.money, True, black, white)
            C_1 = font.render(player1.name +'Credits：%d/%d' % (player1.credit,player1.graduationCredit), True, black, white)
            M_2 = font.render(player2.name +'Money：%d' % player2.money, True, black, white)
            C_2 = font.render(player2.name +'Credits：%d/%d' % (player2.credit,player2.graduationCredit), True, black, white)
            M_3 = font.render(player3.name +'Money：%d' % player3.money, True, black, white)
            C_3 = font.render(player3.name +'Credits：%d/%d' % (player3.credit,player3.graduationCredit), True, black, white)
            M_4 = font.render(player4.name +'Money：%d' % player4.money, True, black, white)
            C_4 = font.render(player4.name +'Credits：%d/%d' % (player4.credit,player4.graduationCredit), True, black, white)
            
            screen.blit(backgroud, (0,0))			
            screen.blit(M_1, (0,0))
            screen.blit(C_1, (0,50))
            screen.blit(M_2, (0,100))
            screen.blit(C_2, (0,150))
            screen.blit(M_3, (0,200))
            screen.blit(C_3, (0,250))
            screen.blit(M_4, (0,300))
            screen.blit(C_4, (0,400))

            blit_alpha(screen, bigdice_image, (1150, 50), image_alpha) # 放骰子  移到右上角		
            textPosition = [MapMessageBoxPosition[0], MapMessageBoxPosition[1]]
            pygame.display.flip()
            clock.tick(60)

            '''
	    # 在每一個地點上，印出血量
            for i in range(1,3): # 1,3要看總共幾個建築，3是機會命運牌
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0].name:
                                text = font.render('%d' % (each.HP), True, red)
                            elif each.owner == allplayers[1].name:
                                text = font.render('%d' % (each.HP), True, white)
                            elif each.owner == allplayers[2].name:
                                text = font.render('%d' % (each.HP), True, black)
                            elif each.owner == allplayers[3].name:
                                text = font.render('%d' % (each.HP), True, blue)
                            else: # 無主地
                                text = font.render('%d'% (each.HP),True, white)
                            screen.blit(text,MapChessPosition_Payment[i])'''
            '''
            for i in range(4, 9): # 9是機會卡
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0].name:
                                text = font.render('%d' % (each.HP), True, red)
                            elif each.owner == allplayers[1].name:
                                text = font.render('%d' % (each.HP), True, green)
                            elif each.owner == allplayers[2].name:
                                text = font.render('%d' % (each.HP), True, black)
                            elif each.owner == allplayers[3].name:
                                text = font.render('%d' % (each.HP), True, black)
                            else: # 無主地
                                text = font.render('%d'% (each.HP),True, white)
                            screen.blit(text, MapChessPosition_Payment[i])'''
            '''
            for i in range(10, 15): # 15是機會卡
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0]:
                                text = font.render('%d' % (each.HP), True, red)
                            elif each.owner == allplayers[1]:
                                text = font.render('%d' % (each.HP), True, green)
                            elif each.owner == allplayers[2]:
                                text = font.render('%d' % (each.HP), True, black)
                            elif each.owner == allplayers[3]:
                                text = font.render('%d' % (each.HP), True, black)
                            else: # 無主地
                                text = font.render('%d'% (each.HP), True, white)
                            screen.blit(text,MapChessPosition_Payment[i])'''
            '''
            for i in range(16,  22): # 16為機會卡
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0]:
                                text = font.render('%d' % (each.HP), True, red)
                            elif each.owner == allplayers[1]:
                                text = font.render('%d' % (each.HP), True, green)
                            elif each.owner == allplayers[2]:
                                text = font.render('%d' % (each.HP), True, black)
                            elif each.owner == allplayers[3]:
                                text = font.render('%d' % (each.HP), True, black)
                            else: # 無主地
                                text = font.render('%d'% (each.HP), True, white)
                            screen.blit(text,MapChessPosition_Payment[i])'''
            '''
            for i in range(23,24): # 24為原點
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0]:
                                text = font.render('%d' % (each.HP), True, red)
                            elif each.owner == allplayers[1]:
                                text = font.render('%d' % (each.HP), True, green)
                            elif each.owner == allplayers[2]:
                                text = font.render('%d' % (each.HP), True, black)
                            elif each.owner == allplayers[3]:
                                text = font.render('%d' % (each.HP), True, blue)
                            else: # 無主地
                                text = font.render('%d'% (each.HP), True, white)
                            screen.blit(text,MapChessPosition_Payment[i])'''

            '''
			# 技能欄，先等公布欄確定怎麼弄再如法炮製
            text0 = font.render("你的技能是:%s"% presentPlayer.PassiveAbility,True, black, white)
            screen.blit(text0, (500,500))#地點亂設	

			# 放置扔出来的骰子
            if player1.dice_value != 0 and showdice:
                screen.blit(dices[player1.dice_value - 1], (70,450))        
					
			# 放置回合结束button
            if showButton2:
                screen.blit(turnover2, TurnOvwrButtonPosition)
            else:
                screen.blit(turnover, TurnOvwrButtonPosition)
					
			# 放置是否button
            if showYes_No == True:
                screen.blit(yes, YesNoMessageBoxPosition[0])
                screen.blit(no, YesNoMessageBoxPosition[1])
            
            for player in allplayers:   # 每回合更新movable & creditable
                player.movable = True
                player.creditable = True

			# 開始蒐集各種觸發事件
            for event in pygame.event.get():
                presentPlayer.showText = ['現在是%s的回合，請擲骰子!結束你的回合請按【回合結束】'] % presentPlayer.name
                printText(presentPlayer)
                
                if event.type == pygame.Quit(): # 按螢幕右上角叉叉
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    if bigdice_rect.collidepoint(event.pos):
                        image_alpha = 255   
                    else:
                        image_alpha = 190

			# 四個玩家要輪流玩，第一位是player1已初始化，但是接下來要判斷!
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bigdice_rect.collidepoint(event.pos):
                        if presentPlayer.movable == True:
                            if presentPlayer == player1:
                                pygame.time.delay(2000) # 故意停一下，假裝骰子在動
                                showYes_No = player1.move(buildings, allplayers)
                                printText(presentPlayer)
                                whetherYes_NoJudge = showYes_No
                                presentPlayer = player2

                            elif presentPlayer == player2:
                                pygame.time.delay(2000)
                                showYes_No = player2.move(buildings, allplayers)
                                printText(presentPlayer)
                                whetherYes_NoJudge = showYes_No
                                presentPlayer = player3

                            elif presentPlayer == player3:
                                pygame.time.delay(2000)
                                showYes_No = player3.move(buildings, allplayers)
                                printText(presentPlayer)
                                whetherYes_NoJudge = showYes_No
                                presentPlayer = player4

                            elif presentPlayer == player4:
                                pygame.time.delay(2000)
                                showYes_No = player4.move(buildings, allplayers)
                                printText(presentPlayer)
                                whetherYes_NoJudge = showYes_No
                                presentPlayer = player1
                        else:
                            pass

                    if whetherYes_NoJudge == True: 
                        if yes_rect.collidepoint(event.pos): # 按是
                            showYes2 = True
                            
                        if no_rect.collidepoint(event.pos): # 按否
                            showNo2  = True       

                if event.type == pygame.MOUSEBUTTONUP:
                    if turnover_rect.collidepoint(event.pos): # 按回合结束
                        showButton2 = False
                    
                    if yes_rect.collidepoint(event.pos): # 按是
                        showYes2 = False
                        showYes_No = False
                        # 只有在可以判定的时候才能算按下了是 同时将判断条件置为空
                        if whetherYes_NoJudge == True:
                            pressYes = True
                            whetherYes_NoJudge = False
                                   
                    if no_rect.collidepoint(event.pos): # 按否
                        showNo2 = False
                        pressYes = False
                        showYes_No = False              
                        whetherYes_NoJudge = False			

            if presentPlayer.isBuyingLand(pressYes) == True:
                pressYes = False
                
            if presentPlayer.isBuildingCastle(pressYes) == True:
                pressYes = False			
								   
												   
							    					   		                  
				 
			#測試用: 按w的話，presentPlayer可以無限移動 (且輪不到其他人)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:#按w，玩家一值動
                    showYes_No = presentPlayer.move(buildings,allplayers)
                    whetherYes_NoJudge = showYes_No

                
            
            
            # 輸贏判斷，遊戲結束
            for each in allplayers:
                font = pygame.font.Font('resource\\font\\myfont.ttf', 200)
                if each.credit == each.graduationCredit:
                    winText = font.render(each.name +'成功畢業了!!', True, red)
                    screen.fill(black)
                    screen.blit(winText,(100,100))
                    font = pygame.font.Font('resource\\font\\myfont.ttf',30)
                    pygame.time.delay(3000)
            
                if each.money < 0:
                    loseText = font.render(each.name +'有錢才能念書!!', True, red)				   
        '''                
        pygame.display.flip()
        clock.tick(60)
            

# 點兩下檔案就會自動開始執行!            
if __name__ == "__main__":
    main()           
