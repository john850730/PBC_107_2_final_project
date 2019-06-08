# -*- coding: utf-8 -*-


#######################################準備工作###############################################

# 初始化模組
import pygame
import random
import sys

# 腳色技能dict
characters_dict = {'土木': {'credit': 140, 'attack': 4, 'ActiveAbility': None, 'PassiveAbility': '收回扣'}, '機械': {'credit': 140, 'attack': 4, 'ActiveAbility': '工具人', 'PassiveAbility': None}, \
    '國企': {'credit': 129, 'attack': 4, 'ActiveAbility': 'elite光環', 'PassiveAbility': None}, '會計': {'credit': 133, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '四萬保底3萬8'}, \
        '經濟': {'credit': 128, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '一隻看不見的手'}, \
            '醫學': {'credit': 229, 'attack': 5, 'ActiveAbility': '妙手回春', 'PassiveAbility': None}, \
                '哲學': {'credit': 128, 'attack': 3, 'ActiveAbility': '你轉系了嗎', 'PassiveAbility': '我唯一知道的，就是我什麼都不知道'}, '中文': {'credit': 128, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '讀書人的事...怎麼能算偷呢'}, \
                    '生科': {'credit': 128, 'attack': 2, 'ActiveAbility': None, 'PassiveAbility': '一日生科，終生ㄎㄎ'}, \
                        '法律': {'credit': 130, 'attack': 3, 'ActiveAbility': None, 'PassiveAbility': '這我一定吉'}}

class Player():
    def __init__(self, image, name, graduationCredit, attack, ActiveAbility, PassiveAbility, definition):
        self.name = name                    # 角色(科系)
        self.money = 10                     # 星星數
        self.credit = 0                     # 目前學分數
        self.graduationCredit = graduationCredit       # 畢業學分數(取決於角色)
        self.attack = attack                 # 攻擊力(取決於角色)
        self.creditable = True              # 每回合結束可否拿學分
        self.isActive = False               # 是否有主動技能
        self.ActiveAbility = ActiveAbility           # 主動技能名稱
        self.PassiveAbility = PassiveAbility          # 被動技能名稱
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
            textline0 = '此角色被動技能為【%s】' % self.PassiveAbility
            textline1 = '擲骰子點數翻倍!'
            self.showText = [textline0, textline1]
        else:
            self.dice_value =  random.randint(1,6)
            self.position += self.dice_value

        if self.position >= 24: # (...)取決於地圖格數
            self.position -= 24
        self.locatedLand = self.judgePosition(lands)
        self.isShowText = True
        return self.eventInPosition(allplayers)#去做到達地要做的事情
    
    
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
        if land.name == '機會命運': # 機會命運的格子
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
        elif land.name == "送到城中校區":
            textLine0 = '搭錯公車，前往城中校區!'
            textLine1 = '停一回合'
            self.movable  = False#不能動一回合
            self.showText = [textLine0,textLine1]
        elif land.name == '女九自助餐':
            textLine0 = '交到女友，攻擊力加1，停一回合'
            self.movable = False
            self.attack += 1
            self.showText = [textLine0]
        elif land.name == '森林系館':
            textLine0 = '加簽到森多概，交到女友，攻擊力加1，停一回合'
            self.movable = False
            self.attack += 1
            self.showText = [textLine0]
            
        else:#走到不是你的土地
            if land.wasBought == False: # 土地未被買時 顯示土地資訊(價格、過路費等等)
                textLine0 = self.name +'骰出了' + '%d' % self.dice_value + '點！'
                textLine1 = self.name +'來到了' + land.name + '!'
                textLine2 = '購買價格：%d' % land.price
                textLine3 = '過路收費：%d' % land.payment
                textLine4 = '是否購買?'
                self.showText = [textLine0, textLine1, textLine2, textLine3, textLine4]
                return True

            elif land.owner == self.name: # 路過自己的土地 蓋城堡
                if land.islocatedCastle == True:#ˇ已經蓋了，不能做事了!
                    textLine0 = "這是你的城堡!"
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
def blit_alpha(target,source,location,opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(),source.get_height())).convert()
    temp.blit(target , (-x , -y))
    temp.blit(source,(0,0))
    temp.set_alpha(opacity)
    target.blit(temp,location)




########################################主函數###############################################    


def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # 初始化
    size = (1270,768)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("台大大富翁")
    
    # 讀取顏色
    textColorInMessageBox = (141,146,152)
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    #font = pygame.font.Font('''''''')
    
    
    # 上傳圖片
    # 基本
    backgroud = pygame.image.load("resource\\pic\\GameMap.png")
    chess = pygame.image.load("resource\\pic\\chess.png")
    chess_com =  pygame.image.load("resource\\pic\\chess1.png")
    bigdice_image = pygame.image.load("resource\\pic\\dice.png").convert_alpha()
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
    StartGameButton = pygame.image.load("resource\\pic\\StartGameButton.png").convert_alpha()
    turnover = pygame.image.load("resource\\pic\\turnover.png")
    turnover2 = pygame.image.load("resource\\pic\\turnover2.png")
    
    #玩家圖檔Image TBD
    imagePlayer0 = pygame.image.load("resource\\pic\\shuaishen.png").convert_alpha()
    imagePlayer1 = pygame.image.load("resource\\pic\\tudishen.png").convert_alpha()
    imagePlayer2 = pygame.image.load("resource\\pic\\caishen.png").convert_alpha()
    imagePlayer3 = pygame.image.load("resource\\pic\\pohuaishen.png").convert_alpha()
    imagePlayer4 = pygame.image.load("resource\\pic\\shuaishen.png").convert_alpha()
    imagePlayer5 = pygame.image.load("resource\\pic\\tudishen.png").convert_alpha()
    imagePlayer6 = pygame.image.load("resource\\pic\\caishen.png").convert_alpha()
    imagePlayer7 = pygame.image.load("resource\\pic\\pohuaishen.png").convert_alpha()
    imagePlayer8 = pygame.image.load("resource\\pic\\shuaishen.png").convert_alpha()
    imagePlayer9 = pygame.image.load("resource\\pic\\tudishen.png").convert_alpha()
    
    
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
    button_rect.left , button_rect.top = 1003,30
    turnover_rect = turnover.get_rect()
    turnover_rect.left , turnover_rect.top = 1035,613
    ce_rect = imagePlayers['土木'].get_rect()
    ce_rect.left , ce_rect.top = 1003,30
    me_rect = imagePlayers['機械'].get_rect()
    me_rect.left , me_rect.top = 1003,30
    ib_rect = imagePlayers['國企'].get_rect()
    ib_rect.left , ib_rect.top = 1003,30
    acct_rect = imagePlayers['會計'].get_rect()
    acct_rect.left , acct_rect.top = 1003,30
    econ_rect = imagePlayers['經濟'].get_rect()
    econ_rect.left , econ_rect.top = 1003,30
    med_rect = imagePlayers['醫學'].get_rect()
    med_rect.left , med_rect.top = 1003,30
    phy_rect = imagePlayers['哲學'].get_rect()
    phy_rect.left , phy_rect.top = 1003,30
    chi_rect = imagePlayers['中文'].get_rect()
    chi_rect.left , chi_rect.top = 1003,30
    bio_rect = imagePlayers['生科'].get_rect()
    bio_rect.left , bio_rect.top = 1003,30
    law_rect = imagePlayers['法律'].get_rect()
    law_rect.left , law_rect.top = 1003,30
	
	

    # 創造玩家
    allplayers = []#共四個角色
    player1 = Player(imagePlayers[name1], name1, characters_dict[name1]["credit"], characters_dict[name1]["attack"]\
		    ,characters_dict[name1]["ActiveAbility"], characters_dict[name1]["PassiveAbility"] )
    allplayers.append(player1)
    player2 = Player(imagePlayers[name2], name2, characters_dict[name2]["credit"], characters_dict[name2]["attack"]\
		    ,characters_dict[name2]["ActiveAbility"], characters_dict[name2]["PassiveAbility"] )
    allplayers.append(player2)
    player3 = Player(imagePlayers[name3], name3, characters_dict[name3]["credit"], characters_dict[name3]["attack"]\
		    ,characters_dict[name3]["ActiveAbility"], characters_dict[name3]["PassiveAbility"] )
    allplayers.append(player3)
    player4 = Player(imagePlayers[name4], name4, characters_dict[name4]["credit"], characters_dict[name4]["attack"]\
		    ,characters_dict[name4]["ActiveAbility"], characters_dict[name4]["PassiveAbility"] )
    allplayers.append(player4)
    presentPlayer = player1#由他開始
    
    # 創造地方:  name, price, payment, location, HP, creditLv
    
 
    gate_Land = Land('大門',0,0,[0],0,"")#沒事
    philo_Land = Land('哲學系館',2,2,[1],3,"low")
    oppChance1 = Land('機會命運',0,0,[2],0,0)
    lita_Land = Land('文學院',2,2,[3],3,"low")
    civ_Land = Land('土木系館',4,3,[4],5,"mid")
    fore_Land = Land('森林系館',0,0,0,[5],"")#停一回合
    engn_Land = Land('工綜',4,3,[6],5,"mid")
    social_Land = Land('社科院',2,4,[7],7,"high")
    law_Land = Land('霖澤館',4,3,[8],5,"mid")
    oppChance2 = Land('機會命運',0,0,[9],0,0)
    hwoDa_Land = Land('活大',6,2,[10],3,"low")
    library_Land = Land('總圖',6,4,[11],7,"high")#
    sea_Land = Land('工科海',4,3,[12],5,"mid")
    mDorm_Land = Land('男一舍',2,2,[13],3,"low")
    oppChance3 = Land('機會命運',0,0,[14],0,0)
    fDorm_Land = Land('女九自助餐',0,0,0,[15],"")#停一回合
    geo_Land = Land("地理系館",6,2,[16],3,"low")
    biosci_Land = Land("生科館",6,2,[17],3,"low")
    mgmt2_Land = Land('管二',6,4,[18],7,"high")
    mgmt1_Land = Land('管一',6,4,[19],7,"high")
    admin_Land = Land('行政大樓',4,3,[20],5,"mid")
    oppChance4 = Land('機會命運',0,0,[21],0,0)
    watermkt_Land = Land('水源市場',6,2,[22],3,"low")
    chengzhon_Land = Land('送往城中校區',0,0,[23],0,"")#暫停一回合
	
	
    
    buildings = [gate_Land,philo_Land,oppChance1,lita_Land,civ_Land,\
                 fore_Land,engn_Land,social_Land,law_Land,oppChance2,hwoDa_Land,\
                 library_Land, sea_Land, mDorm_Land, oppChance3, fDorm_Lan, geo_Land,\
                 biosci_Land, mgmt2_Land, mgmt1_Land, admin_Land, oppChance4,\
                 watermkt_Land, chengzhon_Land]
    
    majorlist = ['土木', '機械', '國企', '會計', '經濟', '醫學', '哲學', '中文', '生科' ,'法律']
	
    
    
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
    
    MapMessageBoxPosition = (474.1 , 276.9)
    YesNoMessageBoxPosition = [(500,438) , (630,438)]
    StartGameButtonPosition = (1003,30)
    TurnOvwrButtonPosition = (1035,613)
    
    
                # 調整位置
    for i in range(0,24):
        MapChessPosition_Original.append((MapXYvalue[i][0]-50,MapXYvalue[i][1]-80))
        MapChessPosition_Player.append((MapXYvalue[i][0]-70,MapXYvalue[i][1]-60))
        MapChessPosition_Com.append((MapXYvalue[i][0]-30,MapXYvalue[i][1]-100))
        MapChessPosition_Payment.append((MapXYvalue[i][0]-30,MapXYvalue[i][1]-15))
    
    
    
        
    
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
    selected = []#選角的時候用
    Medic_Skills_counter = 0#判斷醫學系技能剩下次數
    Medic_harmed_buildings = []		#判斷醫學系受損建築
    
    # 播放背景音樂(暫無)
    # pygame.mixer.music.play(100)
    
########################################遊戲循環開始！###############################################    


   # 循環開始！ 
    while running:
        if not gameStarted:
            if not selectCharacter:
               for event in pygame.event.get():
                   if event.type == pygame.QUIT:
                       sys.exit()
							
                   if event.type == pygame.MOUSEBUTTONDOWN:
						 
                       if button_start.collidepoint(event.pos): # 按下按钮                    
                           SelectCharacter = True  
            screen.blit(GameStart , (0,0))       
            blit_alpha(screen, StartGameButton, StartGameButtonPosition, button_alpha)
			
		#進入選角頁面	
        if selectCharacter:				 
            allset = 0
            selected = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                while allset < 4:
                    if ce_rect.collidepoint(event.pos):
                        selected.append('土木')
                        allset+=1
                    if me_rect.collidepoint(event.pos):
                        selected.append('機械')
                        allset+=1
                    if ib_rect.collidepoint(event.pos):
                        selected.append('國企')
                        allset+=1
                    if acct_rect.collidepoint(event.pos):
                        selected.append('會計')
                        allset+=1
                    if econ_rect.collidepoint(event.pos):
                        selected.append('經濟')
                        allset+=1
                    if econ_med.collidepoint(event.pos):
                        selected.append('醫學')
                        allset+=1
                    if econ_phy.collidepoint(event.pos):
                        selected.append('哲學')
                        allset+=1
                    if chi_rect.collidepoint(event.pos):
                        selected.append('中文')
                    if bio_rect.collidepoint(event.pos):
                        selected.append('生科')
                        allset+=1
                    if law_rect.collidepoint(event.pos):
                        selected.append('法律')
                        allset+=1
			#選好角色	
            name1 = selected[0]
            name2 = selected[1]
            name3 = selected[2]
            name4 = selected[3]
			#遊戲在選完角色自動開始	
            if allset == 4:
                gameStarted = True
            
            #選角介面設定
            screen.blit(selectCharacter , (0,0))#不是很確定selectCharacter?       
            blit_alpha(screen,ce_rect , 'position', 'color')
            blit_alpha(screen,me_rect, 'position', 'color')
            blit_alpha(screen,ib_rect , 'position', 'color')
            blit_alpha(screen,acct_rect , 'position', 'color')
            blit_alpha(screen,econ_rect , 'position', 'color')
            blit_alpha(screen,med_rect , 'position', 'color')
            blit_alpha(screen,phy_rect , 'position', 'color')
            blit_alpha(screen,chi_rect , 'position', 'color')
            blit_alpha(screen,bio_rect , 'position', 'color')
            blit_alpha(screen,law_rect , 'position', 'color')

			#等一下要設定
			#然後也要把每個角色的圖片跟選擇鍵設定好
        if gameStarted:#角色選好後，會變成true
            screen.blit( backgroud , (0,0) )#切換到遊戲背景圖
            blit_alpha(screen, bigdice_image, (50, 600), image_alpha)#放骰子		
            textPosition = [MapMessageBoxPosition[0],MapMessageBoxPosition[1]]#放訊息box 沒blit??
			
	    #印出訊息: ??
            for each in presentPlayer.showText:#?! what is the text??
                text = font.render(each, True, black, textColorInMessageBox)
                screen.blit(text,textPosition)
                textPosition[1] += 30
			
	    #在每一個地點上，印出血量
            for i in range(1,3):#1,3要看總共幾個建築，3是機會命運牌
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0].name:
                                text = font.render('%d' % (each.HP\
														   , True, red)
                            elif each.owner == allplayers[1].name:
								text = font.render('%d' % (each.HP), True, white)
                            elif each.owner == allplayers[2].name:
								text = font.render('%d' % (each.HP)\
														   , True, black)
							elif each.owner == allplayers[3].name:
								text = font.render('%d' % (each.HP)\
														   , True, blue)
							else:#無主地
								text = font.render('%d'% (each.HP),True, white)							
							screen.blit(text,MapChessPosition_Payment[i])
					
			for i in range(4, 9):#9是機會卡
				for each in buildings:
					for every in each.location:
						if i == every:
							if each.owner == allplayers[0].name:
								text = font.render('%d' % (each.HP\
														   , True, red)
							elif each.owner == allplayers[1].name:
								text = font.render('%d' % (each.HP)\
														   , True, green)
							
							elif each.owner == allplayers[2].name:
								text = font.render('%d' % (each.HP)\
														   , True, black)
							elif each.owner == allplayers[3].name:
								text = font.render('%d' % (each.HP)\
							else:#無主地
								text = font.render('%d'% (each.HP),True, white)														   , True, blue)
							screen.blit(text,MapChessPosition_Payment[i]) 
				        
			for i in range(10, 15):#15是機會卡
			    for each in buildings:
					for every in each.location:
						if i == every:
							if each.owner == allplayers[0]:
								text = font.render('%d' % (each.HP\
														   , True, red)
							elif each.owner == allplayers[1]:
								text = font.render('%d' % (each.HP)\
														   , True, green)
							
							elif each.owner == allplayers[2]:
								text = font.render('%d' % (each.HP)\
														   , True, black)
							elif each.owner == allplayers[3]:
								text = font.render('%d' % (each.HP)\
							else:#無主地
								text = font.render('%d'% (each.HP),True, white)														   , True, blue)
							screen.blit(text,MapChessPosition_Payment[i]) 
					
			for i in range(16,  22):#16為機會卡
				for each in buildings:
					for every in each.location:
						if i == every:
							if each.owner == allplayers[0]:
								text = font.render('%d' % (each.HP\
														   , True, red)
							elif each.owner == allplayers[1]:
								text = font.render('%d' % (each.HP)\
								  					     , True, green)
							
							elif each.owner == allplayers[2]:
								text = font.render('%d' % (each.HP)\
														 , True, black)
							elif each.owner == allplayers[3]:
								text = font.render('%d' % (each.HP)\
							else:#無主地
								text = font.render('%d'% (each.HP),True, white)														   , True, blue)
							screen.blit(text,MapChessPosition_Payment[i]) 
					    
		    for i in range(23,24): #24為原點
			    for each in buildings:
					for every in each.location:
						if i == every:
							if each.owner == allplayers[0]:
								text = font.render('%d' % (each.HP\
														   , True, red)
							elif each.owner == allplayers[1]:
								text = font.render('%d' % (each.HP)\
														   , True, green)
							
							elif each.owner == allplayers[2]:
								text = font.render('%d' % (each.HP)\
														   , True, black)
							elif each.owner == allplayers[3]:
								text = font.render('%d' % (each.HP)\
														   , True, blue)
							else:#無主地
								text = font.render('%d'% (each.HP),True, white)
							screen.blit(text,MapChessPosition_Payment[i]
				
			#公佈欄:
			M_1 = font.render(player1.name +'Money：%d' % player1.money, True, black, white)
			C_1 = font.render(player1.name +'Credits：%d/%d' % (player1.credit,player1.graduationCredit), True, black, white)
			M_2 = font.render(player2.name +'Money：%d' % player2.money, True, black, white)
			C_2 = font.render(player2.name +'Credits：%d/%d' % (player2.credit,player2.graduationCredit), True, black, white)
			M_3 = font.render(player3.name +'Money：%d' % player3.money, True, black, white)
			C_3 = font.render(player3.name +'Credits：%d/%d' % (player3.credit,player3.graduationCredit), True, black, white)
			M_4 = font.render(player4.name +'Money：%d' % player4.money, True, black, white)
			C_4 = font.render(player4.name +'Credits：%d/%d' % (player4.credit,player4.graduationCredit), True, black, white)
			
			screen.blit(M_1,(0,0))#還不知道怎麼設定位置!!
			screen.blit(C_1,(0,50))
			screen.blit(M_2,(0,100))
			screen.blit(C_2,(0,150))
			screen.blit(M_3,(0,200))
			screen.blit(C_3,(0,250))
			screen.blit(M_4,(0,300))
			screen.blit(C_4,(0,400))
			
			#技能欄，先等公布欄確定怎麼弄再如法炮製
			text0 = font.render("你的技能是:%s"% presentPlayer.PassiveAbility,True, black, white)
			screen.blit(text0,(500,500))#地點亂設			
			# 放置扔出来的骰子
			if player_1.dice_value != 0 and showdice:
				screen.blit(dices[player_1.dice_value - 1],(70,450))        
					
			# 放置回合结束button
			if showButton2:
				screen.blit(turnover2,TurnOvwrButtonPosition)
			else:
				screen.blit(turnover,TurnOvwrButtonPosition)
					
			# 放置是否button
			if showYes_No == True:
				screen.blit(yes , YesNoMessageBoxPosition[0])
				screen.blit(no  , YesNoMessageBoxPosition[1])

			#開始蒐集各種觸發事件
			for event in pygame.event.get():
				if event.type == pygame.Quit():#按螢幕右上角叉叉
					sys.exit()
			
			#四個玩家要輪流玩，第一位是player1已初始化，但是接下來要判斷!    
				if event.type == pygame.MOUSEBUTTONDOWN:
					if bigdice_rect.collidepoint(event.pos):#怪怪的，應該是按下next turn 才判斷?
						presentPlayer = allplayers[playerCount]
						if presentPlayer.movable:#有時候會被設為False
							pygame.time.delay(2000)#故意停一下，假裝骰子在動
							if presentPlayer.name == "哲學":
						    		if presentPlayer.credit >= 50:
							#主動技能
								textline0 = '此角色有主動技能為【%s】' % presentPlayer.ActiveAbility
								textline1 = '選擇轉系必須付出30%的學分!警告: 轉系是隨機事件!'
								presentPlayer.showText = [textline0, textline1]
							
							whetheryesnojudge = True
							showYes_No = True
							if pressYes == True:
								presentPlayer.credit = presentPlayer.credit*0.7
								majortemp = random.randint(0,9)
								while majortemp == 5 or majortemp == 6:
									majortemp =random.randint(0,9)
									
								presentPlayer.name = majorlist[majortemp]
								textline3 = '妳/你成功變成%s' % presentPlayer.name
								textline4 = '哈哈哈'
								presentPlayer.showText.append([textline3, textline4])
								presentPlayer.showText.pop([textline0, textline1])
						     else:
							       pass
									
							textline5 = '此角色被動技能為【%s】' % presentPlayer.PassiveAbility
							textline6 = '擲骰子點數翻倍!'
							presentPlayer.showText.append([textline5, textline6])
							for each in presentPlayer.showText:
								text = font.render(each, True, white, textColorInMessageBox)
								screen.blit(text,textPosition)
								textPosition[1] += 30
							showYes_No = presentPlayer.move(buildings,allplayers)#這一步會丟骰子，並移動地點，並觸發到達目的地後會發生的事件。
							whetherYes_NoJudge = showYes_No
												   
							if presentPlayer.name == "醫學":
								if Medic_Skills_counter < 2:
									if len(presentPlayer.ownedLands) == 1 and presentPlayer.ownedLands[0].hp < presentPlayer.ownedLands[0].temp_hp:
							   		textline0 = '此角色有主動技能為【%s】' % presentPlayer.ActiveAbility
							   		textline1 = '是否使用妙手回春？注意！ 妙手回春有使用限制'
							   		presentPlayer.showText = [textline0, textline1]
							   		whetheryesnojudge = True
							   		showYes_No = True
							   		if pressYes == True:	
							       			presentPlayer.ownedLands[0].hp = presentPlayer.ownedLands[0].temp_hp
							       			Medic_Skills_counter += 1
							       			textline3 = '你/妳受損的建築已回復'	
							       			presentPlayer.showText = [textline3]					   
								if len(presentPlayer.ownedLands) > 1:
							    		for i in range(len(presentPlayer.owendLands)):
							        if presentPlayer.ownedLands[i].HP < presentPlayer.ownedLands[i].temp_HP:
								   Medic_harmed_buildings.append(i)				   
                                                            	if len(Medic_harmed_buildings) > 0:
									textline0 = '此角色有主動技能為【%s】' % presentPlayer.ActiveAbility
							       		textline1 = '是否使用妙手回春？注意！ 妙手回春有使用限制'
							       		presentPlayer.showText = [textline0, textline1]
							       		whetheryesnojudge = True
							       		showYes_No = True
							       		if pressYes == True:	
								        	which_to_heal = random.randit(0,24)
								        	while which_to_heal not in  Medic_harmed_buildings:
								            	which_to_heal = random.randit(0,24)
								        	presentPlayer.ownedLands[which_to_heal].hp = presentPlayer.ownedLands[which_to_heal].temp_hp
							            	Medic_Skills_counter += 1
								    	textline3 = '你/妳受損的建築已回復'	
							            	presentPlayer.showText = [textline3]
						
						
						for each in presentPlayer.showText:#都到這裡才印太晚了，前面就該開始印了，可以做成fcn?
						    	text = font.render(each, True, white, textColorInMessageBox)
							screen.blit(text,textPosition)
							textPosition[1] += 30
							showYes_No = presentPlayer.move(buildings,allplayers)#這一步會丟骰子，並移動地點，並觸發到達目的地後會發生的事件。
							whetherYes_NoJudge = showYes_No						   
												   
							    					   
							   					   
							    					   
					if presentPlayer.name != "哲學" and presentPlayer.name != "醫學":
						showYes_No = presentPlayer.move(buildings,allplayers)#這一步會丟骰子，並移動地點，並觸發到達目的地後會發生的事件。
						whetherYes_NoJudge = showYes_No
							
					else:
						 continue#回去看
				#按回合結束鍵，更新presentPlayer是誰     
				if turnover_rect.collidepoint(event.pos): 
					showButton2 = True #what is this??
					playerCount += 1
					if playerCount == 4:
						playerCount -= 4  
								  
				else:#什麼都沒按
					showButton2 = False #what is this  
			
			if whetherYes_NoJudge == True:#是否有效 
				if yes_rect.collidepoint(event.pos): # 按Yes
					showYes2 = True
									
				if no_rect.collidepoint(event.pos): # 按No
					showNo2  = True
		  
			if event.type == pygame.MOUSEBUTTONUP:#按完之後，發生的事
							
				if turnover_rect.collidepoint(event.pos): # 按回合结束
					showButton2 = False
							
				if yes_rect.collidepoint(event.pos): # 按是否
					showYes2 = False#1 or 2 只是表示按鍵突出還是往下
					showYes_No = False
								
				if whetherYes_NoJudge == True:
					pressYes = True#才算是
					whetherYes_NoJudge = False#重新
					  
				if no_rect.collidepoint(event.pos): # 按是否
					showNo2 = False
					pressYes = False
					showYes_No = False              
					whetherYes_NoJudge = False               
				 
			#測試用: 按w的話，presentPlayer可以無限移動 (且輪不到其他人)       
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:#按w，玩家一值動
					showYes_No = presentPlayer.move(buildings,allplayers)
					whetherYes_NoJudge = showYes_No
					
			if presentPlayer.isBuyingLand(pressYes) == True:#不懂這裡的功能
						pressYes = False
						
			if presentPlayer.isBuildingCastle(pressYes) == True:
						pressYes = False
			if presentPlayer.isAttacking(pressYes) == True:
						pressYes = False
			 ##########################################################
		 
                    
            
                    
                    
            # 放置玩家位置，若兩個玩家到同一個地方，自動將一個玩家挪動位置。
            for each in players:
                for every in computers:
                    if each.position == every.position:
                        screen.blit(each.image,MapChessPosition_Player[each.position])
                        screen.blit(every.image,MapChessPosition_Com[every.position])
                        each.temp_position = True
                        every.temp_position = True
                        
            for each in players:
                if each.temp_position == False:
                    screen.blit(each.image,MapChessPosition_Original[each.position])
                    each.temp_position = True
                each.temp_position = not each.temp_position
                
                  
            for every in computers:
                if every.temp_position == False:
                    screen.blit(every.image,MapChessPosition_Original[every.position])
                    every.temp_position = True
                every.temp_position = not every.temp_position
                
            
            
            # 輸贏判斷，遊戲結束
            for each in allplayers:
            font = pygame.font.Font('resource\\font\\myfont.ttf',200)
                if each.credit == each.graduationCredit:
                    winText = font.render(each.name +'成功畢業了!!', True, red)
                    screen.fill(black)
                    screen.blit(winText,(100,100))
                    font = pygame.font.Font('resource\\font\\myfont.ttf',30)            
                    pygame.time.delay(3000)
		if each.money < 0:
			loseText = font.render(each.name +'有錢才能念書!!', True, red)
			
		
		
		    
												   
												   
                        
        # 畫面執行
        
        pygame.display.flip()
        clock.tick(60)              # 刷新率
    
            

# 點兩下檔案就會自動開始執行!            
if __name__ == "__main__":
    main()           
