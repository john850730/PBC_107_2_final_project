# -*- coding: utf-8 -*-

########################################準備工作###############################################

# 初始化
import pygame
import random
import sys

characters_dict = \
   {'土木': {'credit': 140, 'attack': 4, 'ActiveAbility': '無', 'PassiveAbility': '收回扣', 'definition': '買完土地、或建蓋城堡後，可以回收10%消耗的錢幣'}, \
    '機械': {'credit': 140, 'attack': 4, 'ActiveAbility': '無', 'PassiveAbility': '工具人', 'definition': '蓋城堡時可直接升級城堡血量10點'}, \
    '國企': {'credit': 129, 'attack': 4, 'ActiveAbility': '無', 'PassiveAbility': '真●Elite', 'definition': '遊戲介面上的角色發出光芒一下下'}, \
    '會計': {'credit': 133, 'attack': 3, 'ActiveAbility': '無', 'PassiveAbility': '四萬保底3萬8', 'definition': '每回合自動獲得2錢幣'}, \
    '經濟': {'credit': 128, 'attack': 3, 'ActiveAbility': '無', 'PassiveAbility': '一隻看不見的手', 'definition': '土地被其他玩家踩到時，可偷取對方10%的錢幣'}, \
    '醫學': {'credit': 229, 'attack': 5, 'ActiveAbility': '妙手回春', 'PassiveAbility': '在座的各位都是垃X', 'definition': '在該角色回合開始時，可選擇是否使用妙手回春，選擇任一擁有的一棟建築，回覆該建築物至滿血狀態(每場遊戲只能使用一次)'}, \
    '哲學': {'credit': 128, 'attack': 3, 'ActiveAbility': '你轉系了嗎', 'PassiveAbility': '我唯一知道的，就是我什麼都不知道', 'definition': '擲骰子的點數翻倍'}, \
    '中文': {'credit': 128, 'attack': 3, 'ActiveAbility': '無', 'PassiveAbility': '讀書人的事...怎麼能算偷呢', 'definition': '對方玩家經過我土地(含城堡)時，除了收取過路費外，還可以偷取對方1錢幣'}, \
    '生科': {'credit': 128, 'attack': 2, 'ActiveAbility': '無', 'PassiveAbility': '一日生科，終生顆顆', 'definition': '對方玩家攻擊該玩家的土地或城堡，每次只會受到2點傷害'}, \
    '法律': {'credit': 130, 'attack': 3, 'ActiveAbility': '無', 'PassiveAbility': '這我一定吉', 'definition': '法律系所持有城堡被打下時，扣除打下者10%的錢幣'}}

# 定義物件等
class Player():
    def __init__(self, image ,name , isPlayer, PassiveAbility):
        self.name = name
        self.money = 10000
        self.isGoingToMove = False 
        self.movable = True
        self.small_image = image
        self.position = 0  
        self.temp_position = False
        self.dice_value = 0
        self.locatedBuilding = 0
        self.showText = []
        self.isPlayer = isPlayer
        self.ownedBuildings = []
        self.isShowText = False
        self.soundPlayList = 0
        self.moneyLucky = 0
        self.shuaishen = 0
        self.landLucky = 0
        self.waterUncle = 0
        self.PassiveAbility = PassiveAbility
        
    
    def judgePosition(self,buildings): 
        """判斷位置，回傳所在位置的建築"""
        for each in buildings:
            for every in each.location:
                if self.position == every:
                    return each
                    
         
    def buyaBuilding(self,isPressYes):
        """出現是否購買時，按下Yes按鈕""" 
        if isPressYes and self.locatedBuilding.owner != self.name:
            self.locatedBuilding.owner = self.name
            self.locatedBuilding.wasBought = True
            self.ownedBuildings.append(self.locatedBuilding)
            self.money -= self.locatedBuilding.price
            self.showText = [self.name + '購買了' + self.locatedBuilding.name + '!']
            return True
        else:
            return False
        
          
            
    def addaHouse(self,isPressYes): 
        """出現是否升級時，按下Yes"""
        try:
            if isPressYes and self.locatedBuilding.owner == self.name:
                self.locatedBuilding.builtRoom += 1
                self.money -= self.locatedBuilding.payment
                self.showText = [self.name + '在' + self.locatedBuilding.name + '上!','蓋了一座房子！',\
                                '有%d' % self.locatedBuilding.builtRoom + '個房子了！',\
                                "它的過路費是%d" % (self.locatedBuilding.payment * \
                                                (self.locatedBuilding.builtRoom + 1)) ]
                self.soundPlayList = 2
                return True
            else:
                return False
        except:
            pass
    
    def move(self,buildings,allplayers):
        """按下骰子後，腳色移動，移動後，根據所在地進入eventInPosition函數"""	
        self.dice_value =  random.randint(1,6)
        self.position += self.dice_value
        if self.position >= 24:
            self.position -= 24
        self.locatedBuilding = self.judgePosition(buildings)
        self.isShowText = True
        return self.eventInPosition(allplayers)
    
    
    def eventInPosition(self,allplayers):
        """判斷所在位置要做甚麼事情"""	
        building = self.locatedBuilding
        if building.name != '機會命運':
            if self.locatedBuilding.wasBought == False: 
            #無主地，列印價格資訊
                if self.isPlayer == True:
                    textLine0 = self.name +'骰出' + '%d' % self.dice_value + '點！'
                    textLine1 = self.name +'來到' + building.name + '!'
                    textLine2 = '購買價格：%d' % building.price
                    textLine3 = '過路收費：%d' % building.payment
                    textLine4 = '是否購買?'
                    self.showText = [textLine0,textLine1,textLine2,textLine3,textLine4]
                    return True
                else :
                    self.addaHouse(not self.buyaBuilding(True))
                    
            elif building.owner == self.name: 
                #是自己的土地，可以選擇是否加蓋
                if self.waterUncle == 1:
                    textLine0 = self.name + '遇到水源阿伯！'
                    textLine1 = '你的房子被拖走了QQ！'
                    building.owner = 'no'
                    building.wasBought = False
                    self.showText = [textLine0,textLine1]
                    self.waterUncle = 0
                else:
                    if self.isPlayer == True:
                        textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                        textLine1 = '來到了'+ self.locatedBuilding.name +'!'
                        textLine2 = '可以加蓋系館！' 
                        textLine3 = '加蓋需要費用：%d' % building.payment
                        textLine4 = '是否加蓋呢?'
                        self.showText = [textLine0,textLine1,textLine2,textLine3,textLine4]
                        return True
                    else:
                        self.addaHouse(True)
            else:
                """所在地為其他人的土地"""
                for each in allplayers: 
                #到別人的土地或建築，就要被收過路費
                #加入運氣成分，三種事件
                    if self.locatedBuilding.owner == each.name and each.name != self.name:
                        if self.moneyLucky == 1:
                            textLine0 = self.name + '人脈大增，大家都是你的好朋友!!'
                            textLine1 = '免除過路費%d！' % (building.payment * (building.builtRoom + 1))
                            self.showText = [textLine0,textLine1]
                            self.moneyLucky = 0
                        else:
                            if self.landLucky == 1:
                                textLine0 = self.name + '使用【新體NPC】真傳！'
                                textLine1 = '強佔土地！'
                                textLine2 = building.name + '現在屬於'+ self.name
                                self.locatedBuilding.owner = self.name
                                self.showText = [textLine0,textLine1,textLine2]
                                self.landLucky = 0
                            else:
                                if self.waterUncle == 1:
                                    textLine0 = self.name + '使用【水源阿伯】真傳！'
                                    textLine1 = '對手的建築房子被拖走了！'
                                    building.owner = 'no'
                                    building.wasBought = False
                                    self.showText = [textLine0,textLine1]
                                    self.waterUncle = 0   
                                else:
                                    textLine0 = self.name + '骰出了' + '%d'% self.dice_value + '點！'
                                    textLine1 = self.name+ '來到了'+ each.name+'的'  
                                    textLine2 = '【%s】' % building.name + ',被收費!'
                                    if self.shuaishen == 1:
                                        textLine3 = '過路收費：%d*2!' % (building.payment * (building.builtRoom + 1)*2)
                                        self.shuaishen = 0
                                    else:
                                        textLine3 = '過路收費：%d' % (building.payment * (building.builtRoom + 1))
                                    textLine4 = '幫QQ！'+ self.name +'好口憐！'
                                    self.showText = [textLine0,textLine1+textLine2,textLine3,textLine4]
                                    # 收費！
                                    self.money -= building.payment * (building.builtRoom + 1)
                                    each.money += building.payment * (building.builtRoom + 1)
                                    self.soundPlayList = 3

                        
        else:
            """所在地為機會命運，抽到的人會進入那個狀態，當走到別人土地時會生效(並reset)"""
            whichone = self.dice_value % 4#也是random
            if whichone == 0:
                self.moneyLucky = 1
                textLine2 = '遇到了財神！'
                textLine3 = '免一次過路費！'
            if whichone == 1:
                self.shuaishen = 1
                textLine2 = '遇到了衰神！'
                textLine3 = '過路費加倍一次！'
            if whichone == 2:
                self.landLucky = 1
                textLine2 = '得到【新體NPC】真傳！'
                textLine3 = '強佔一次房子！'
            if whichone == 3:
                self.waterUncle = 1
                textLine3 = '摧毀路過的房子！'
                textLine2 = '得到【水源阿伯】真傳！'
            textLine0 = self.name +'骰出了' +'%d'% self.dice_value + '點！'
            textLine1 = '來到了機會命運！'
            self.showText = [textLine0,textLine1,textLine2,textLine3]


    
    
    
class Building():                           
    def __init__(self,name,price,payment,location):
        self.name = name
        self.price = price
        self.payment = payment
        self.location = location
        self.wasBought = False               
        self.builtRoom = 0                   
        self.owner = 'no'
    
    



def blit_alpha(target,source,location,opacity):
    #用來繪製按鍵深淺
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
    
    # 初始化屏幕
    size = (1270,768)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("臺大戰系比武大會")
    
    # 上傳字體與顏色
    textColorInMessageBox = (141,146,152)
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)
    font = pygame.font.Font('resource\\font\\tradition.ttf',30)
    
    
    # 上傳各種圖檔
    background = pygame.image.load("resource\\pic\\GameMap.png")
    background = pygame.transform.scale(background, (1270,768))
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
    dice_1 = pygame.transform.scale(dice_1, (60,60))
    dice_2 = pygame.transform.scale(dice_2, (60,60))
    dice_3 = pygame.transform.scale(dice_3, (60,60))
    dice_4 = pygame.transform.scale(dice_4, (60,60))
    dice_5 = pygame.transform.scale(dice_5, (60,60))
    dice_6 = pygame.transform.scale(dice_6, (60,60))
    dices = [dice_1,dice_2,dice_3,dice_4,dice_5,dice_6]
    yes = pygame.image.load("resource\\pic\\yes.png")
    yes = pygame.transform.scale(yes, (50,50))
    yes2 = pygame.image.load("resource\\pic\\yes2.png")
    yes2 = pygame.transform.scale(yes2, (50,50))
    no = pygame.image.load("resource\\pic\\no.png")
    no = pygame.transform.scale(no, (50,50))
    no2 = pygame.image.load("resource\\pic\\no2.png")
    no2 = pygame.transform.scale(no2, (50,50))
    GameStart = pygame.image.load("resource\\pic\\GameStart.png")
    GameStart = pygame.transform.scale(GameStart, (1270,768))
    StartGameButton = pygame.image.load("resource\\pic\\StartGameButton.png").convert_alpha()
    StartGameButton = pygame.transform.scale(StartGameButton, (600,125))
    turnover = pygame.image.load("resource\\pic\\turnover.png")
    turnover = pygame.transform.scale(turnover, (220,140))
    turnover2 = pygame.image.load("resource\\pic\\turnover2.png")
    turnover2 = pygame.transform.scale(turnover2, (220,140))
    shuaishen = pygame.image.load("resource\\pic\\shuaishen.png").convert_alpha()
    shuaishen = pygame.transform.scale(shuaishen, (60,60))
    landLucky = pygame.image.load("resource\\pic\\landLucky.png").convert_alpha()
    landLucky = pygame.transform.scale(landLucky, (60,60))
    moneyLucky = pygame.image.load("resource\\pic\\moneyLucky.png").convert_alpha()
    moneyLucky = pygame.transform.scale(moneyLucky, (60,60))
    waterUncle = pygame.image.load("resource\\pic\\waterUncle.png").convert_alpha()
    waterUncle = pygame.transform.scale(waterUncle, (60,60))

    
    #玩家圖檔Image 
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
    #遊戲開始後的小人像
    imagePlayer0_small = pygame.transform.scale(imagePlayer0, (80, 60))
    imagePlayer1_small = pygame.transform.scale(imagePlayer1, (80, 60))
    imagePlayer2_small = pygame.transform.scale(imagePlayer2, (80, 60))
    imagePlayer3_small = pygame.transform.scale(imagePlayer3, (80, 60))
    imagePlayer4_small = pygame.transform.scale(imagePlayer4, (80, 60))
    imagePlayer5_small = pygame.transform.scale(imagePlayer5, (80, 60))
    imagePlayer6_small = pygame.transform.scale(imagePlayer6, (80, 60))
    imagePlayer7_small = pygame.transform.scale(imagePlayer7, (80, 60))
    imagePlayer8_small = pygame.transform.scale(imagePlayer8, (80, 60))
    imagePlayer9_small = pygame.transform.scale(imagePlayer9, (80, 60))
	
    small_image = {"土木":imagePlayer0_small, "機械":imagePlayer1_small, "國企":imagePlayer2_small, '會計':imagePlayer3_small, '經濟':imagePlayer4_small\
		   ,'醫學':imagePlayer5_small, '哲學':imagePlayer6_small, '中文':imagePlayer7_small, '生科':imagePlayer8_small, '法律':imagePlayer9_small}
    imagePlayers = {"土木":imagePlayer0, "機械":imagePlayer1, "國企":imagePlayer2, '會計':imagePlayer3, '經濟':imagePlayer4\
		   ,'醫學':imagePlayer5, '哲學':imagePlayer6, '中文':imagePlayer7, '生科':imagePlayer8, '法律':imagePlayer9}#dictionary of images of players, keys = "name"

    
    # 各種rect 
    bigdice_rect = bigdice_image.get_rect()
    bigdice_rect.left , bigdice_rect.top = 1066, 55
    yes_rect = yes.get_rect()
    yes_rect.left , yes_rect.top = 600, 495
    no_rect = no.get_rect()
    no_rect.left , no_rect.top =  700, 495
    button_rect = StartGameButton.get_rect()
    button_rect.left , button_rect.top = 370, 65
    turnover_rect = turnover.get_rect()
    turnover_rect.left , turnover_rect.top = 1040, 550
    
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
    
    
    # 創造各種建築:name,price,payment,location
    gate_Land = Building('大門',0,0,[0]) 
    philo_Land = Building('哲學系館',200,200,[23])
    oppChance1 = Building('機會命運',0,0,[22])
    lita_Land = Building('文學院',200,200,[21])
    civ_Land = Building('土木系館',400,300,[20])
    fore_Land = Building('森林系館',0,0,[19]) 
    engn_Land = Building('工綜',400,300,[18])
    social_Land = Building('社科院',200,400,[17])
    law_Land = Building('霖澤館',400,300,[16])
    oppChance2 = Building('機會命運',0,0,[15])
    hwoDa_Land = Building('活大',600,200,[14])
    library_Land = Building('總圖',600,400,[13])
    sea_Land = Building('工科海',400,300,[12])
    mDorm_Land = Building('男一舍',200,200,[11])
    oppChance3 = Building('機會命運',0,0,[10])
    fDorm_Land = Building('女九自助餐',0,0,[9]) 
    geo_Land = Building("地理系館",600,200,[8])
    biosci_Land = Building("生科館",600,200,[7])
    mgmt2_Land = Building('管二',600,400,[6])
    mgmt1_Land = Building('管一',600,400,[5])
    admin_Land = Building('行政大樓',400,300,[4])
    oppChance4 = Building('機會命運',0,0,[3])
    watermkt_Land = Building('水源市場',600,200,[2])
    chengzhon_Land = Building('送往城中校區',500,100,[1]) 
	
	
    
    buildings = [chengzhon_Land, watermkt_Land, oppChance4, admin_Land, \
                mgmt1_Land, mgmt2_Land, biosci_Land, geo_Land, fDorm_Land,\
                oppChance3, mDorm_Land, sea_Land, library_Land, hwoDa_Land,\
                oppChance2, law_Land, social_Land, engn_Land, fore_Land,\
                civ_Land, lita_Land, oppChance1, philo_Land, gate_Land]
    
    
    
    # 座標，之後方便用
    MapXYvalue = [(127,392), (127,485), (127,584), (225,584), (323,584),\
                  (421,584), (519,584), (617,584), (715,584), (813,584),\
                  (813,485), (813,392), (813,296), (813,200), (813,104),\
                  (715,104), (617,104), (519,104), (421,104), (323,104),\
                  (225,104), (127,104), (127,200), (127,296)]
    
    MapChessPosition_Player = []
    MapChessPosition_Com = []
    MapChessPosition_Original = []
    MapChessPosition_Payment = []
    
    MapMessageBoxPosition = (280, 400)
    YesNoMessageBoxPosition = [(600, 495) , (700, 495)]
    StartGameButtonPosition = (370, 65)
    TurnOvwrButtonPosition = (1040, 550)
    
    
    for i in range(0,24):
        MapChessPosition_Original.append((MapXYvalue[i][0]-50,MapXYvalue[i][1]-80))
        MapChessPosition_Player.append((MapXYvalue[i][0]-10,MapXYvalue[i][1]-40))
        MapChessPosition_Com.append((MapXYvalue[i][0]+40,MapXYvalue[i][1]-40))
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
    showButton2 = False
    selectCharacter = False
    

    
########################################Game loop###############################################    



    while running:
        if not gameStarted:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                 
                if event.type == pygame.MOUSEMOTION:
                    if button_rect.collidepoint(event.pos):
                        button_alpha = 255   
                    else:
                        button_alpha = 120 
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                     
                    if button_rect.collidepoint(event.pos):                     
                        gameStarted = True
                        selectCharacter = True  
            
            screen.blit(GameStart , (0,0))#第一個頁面       
            blit_alpha(screen, StartGameButton, StartGameButtonPosition, button_alpha)
            font = pygame.font.Font('resource\\font\\tradition.ttf', 150)
            text = font.render('臺大戰系比武大會', True, white)
            screen.blit(text, (210, 370))
            font = pygame.font.Font('resource\\font\\tradition.ttf', 30)

        
        if selectCharacter:
            button_alpha = 255
            selection_dict = {'機械': [(42, 150), button_alpha], '土木': [(292, 150), button_alpha],\
                            '國企': [(542, 150), button_alpha], '會計': [(792, 150), button_alpha],\
                            '經濟': [(1037, 150), button_alpha], '醫學': [(42, 420), button_alpha],\
                            '哲學': [(292, 420), button_alpha], '中文': [(542, 420), button_alpha],\
                            '生科': [(792, 420), button_alpha], '法律': [(1037, 420), button_alpha]}
            
            def selection_blit(diction): # 角色科系印出的函數
                screen.blit(character_selection, (0,0))#第二個頁面(選角)
                for key in diction:
                    blit_alpha(screen, imagePlayers[key], diction[key][0], diction[key][1])
                font = pygame.font.Font('resource\\font\\tradition.ttf', 50)
                text1 = font.render('選好你認為最會戰的系', True, red)
                text2 = font.render(' 以及 ', True, red)
                text3 = font.render('你最想戰的系所吧!', True, red)
                screen.blit(text1, (530, 0))
                screen.blit(text2, (660, 50))
                screen.blit(text3, (530, 100))
                font = pygame.font.Font('resource\\font\\tradition.ttf', 30)
                pygame.display.flip()
                clock.tick(60)
            
            selection_blit(selection_dict)
            
            
            allset = 0
            selected = []
            while allset < 2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if ce_rect.collidepoint(event.pos):
                            selection_dict['土木'][1] = 100                       
                            selected.append('土木')
                            allset += 1
                            selection_blit(selection_dict)

                        if me_rect.collidepoint(event.pos):
                            selection_dict['機械'][1] = 100                           
                            selected.append('機械')
                            allset += 1
                            selection_blit(selection_dict)

                        if ib_rect.collidepoint(event.pos):
                            selection_dict['國企'][1] = 100                           
                            selected.append('國企')
                            allset += 1
                            selection_blit(selection_dict)

                        if acct_rect.collidepoint(event.pos):
                            selection_dict['會計'][1] = 100                           
                            selected.append('會計')
                            allset += 1
                            selection_blit(selection_dict)

                        if econ_rect.collidepoint(event.pos):
                            selection_dict['經濟'][1] = 100                          
                            selected.append('經濟')
                            allset += 1
                            selection_blit(selection_dict)

                        if med_rect.collidepoint(event.pos):
                            selection_dict['醫學'][1] = 100                         
                            selected.append('醫學')
                            allset += 1
                            selection_blit(selection_dict)

                        if phy_rect.collidepoint(event.pos):
                            selection_dict['哲學'][1] = 100                          
                            selected.append('哲學')
                            allset += 1
                            selection_blit(selection_dict)

                        if chi_rect.collidepoint(event.pos):
                            selection_dict['中文'][1] = 100                           
                            selected.append('中文')
                            allset += 1
                            selection_blit(selection_dict)

                        if bio_rect.collidepoint(event.pos):
                            selection_dict['生科'][1] = 100                           
                            selected.append('生科')
                            allset += 1
                            selection_blit(selection_dict)

                        if law_rect.collidepoint(event.pos):
                            selection_dict['法律'][1] = 100                            
                            selected.append('法律')
                            allset += 1
                            selection_blit(selection_dict)

            #創建腳色
            players = []
            computers = []
            allplayers = []
            name1 = selected[0]
            name2 = selected[1]
            player_1 = Player(small_image[name1] , name1, True, characters_dict[name1]['PassiveAbility'])
            player_com1 = Player(small_image[name2], name2, False, characters_dict[name2]['PassiveAbility'])
            players.append(player_1)
            computers.append(player_com1)
            allplayers.append(player_1)
            allplayers.append(player_com1)
    
            presentPlayer = player_com1
            selectCharacter = False
        
        if gameStarted:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEMOTION:
                    if bigdice_rect.collidepoint(event.pos):
                        image_alpha = 255   
                    else:
                        image_alpha = 190
                        
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if bigdice_rect.collidepoint(event.pos): # 按骰子
                        if presentPlayer != player_1:
                            pygame.time.delay(1000)
                            showYes_No = player_1.move(buildings,allplayers)
                            whetherYes_NoJudge = showYes_No
                            presentPlayer = player_1
                        else:
                            presentPlayer.showText = ['還沒到%s的回合！' % (player_1.name)]
                        
                    if turnover_rect.collidepoint(event.pos): # 按回合结束
                        showButton2 = True
                        if presentPlayer != player_com1:
                            showYes_No = player_com1.move(buildings,allplayers)
                            presentPlayer = player_com1
                        else:
                            presentPlayer.showText = ['還沒到%s的回合！請%s擲骰子！' % (presentPlayer.name, player_1.name)]                            
                    else:
                        showButton2 = False
                    
                        # 不顯示Yes_No的時不能點擊！
                    if whetherYes_NoJudge == True: 
                        if yes_rect.collidepoint(event.pos): # 按是否
                            showYes2 = True
                            
                        if no_rect.collidepoint(event.pos): # 按是否
                            showNo2  = True
                      
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if turnover_rect.collidepoint(event.pos): # 按回合结束
                        showButton2 = False
                    
                    if yes_rect.collidepoint(event.pos): # 按是否
                        showYes2 = False
                        showYes_No = False
                        
                        if whetherYes_NoJudge == True:
                            pressYes = True
                            whetherYes_NoJudge = False
                            
                            
                    if no_rect.collidepoint(event.pos): # 按是否
                        showNo2 = False
                        pressYes = False
                        showYes_No = False              
                        whetherYes_NoJudge = False        
            
                # 測試選項用        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        showYes_No = player_1.move(buildings,allplayers)
                        whetherYes_NoJudge = showYes_No
                        presentPlayer = player_1
                    if event.key == pygame.K_q:
                        showYes_No = player_com1.move(buildings,allplayers)
                        presentPlayer = player_com1
            
             
            # 購買的按鍵還原
            
            if presentPlayer.buyaBuilding(pressYes) == True:
                pressYes = False
                
            if presentPlayer.addaHouse(pressYes) == True:
                pressYes = False
            
                
            
                
                    
                
  ##############################################################################################            
            screen.blit(background , (0,0))#第三頁(遊戲介面)
            blit_alpha(screen, bigdice_image, (1066, 55), image_alpha)

            P_1 = font.render('玩家: %s系, 名言:【%s】' % (player_1.name, player_1.PassiveAbility), True, blue, None)
            P_2 = font.render('電腦: %s系, 名言:【%s】' % (player_com1.name, player_com1.PassiveAbility), True, red, None)

            screen.blit(P_1, (230,225))
            screen.blit(P_2, (230,295))
            
            
            textPosition = [MapMessageBoxPosition[0], MapMessageBoxPosition[1]]
            
            # 印出遊戲資訊
            font = pygame.font.Font('resource\\font\\tradition.ttf', 35)
            for each in presentPlayer.showText:
                text = font.render(each, True, black)
                screen.blit(text,textPosition)
                textPosition[1] += 30
            font = pygame.font.Font('resource\\font\\tradition.ttf', 30)

                
            # 在每個位置上顯示過路費
            def landsNameHP(buildings, MapXYvalue):
                font = pygame.font.Font('resource\\font\\tradition.ttf', 23)
                for building, coordinate in zip(buildings, MapXYvalue):
                    if len(building.name) >= 4:
                        text1 = font.render(building.name[0:2], True, black, None)
                        text2 = font.render(building.name[2:len(building.name)], True, black, None)
                        if building.owner == player_1.name:
                            text3 = font.render(player_1.name + str(building.payment * (building.builtRoom + 1)), True, blue, None)
                        elif building.owner == player_com1.name:
                            text3 = font.render(player_com1.name + str(building.payment * (building.builtRoom + 1)), True, red, None)
                        else:
                            text3 = font.render('(無主地)', True, black, None)
                        screen.blit(text1, coordinate)
                        screen.blit(text2, (coordinate[0], coordinate[1]+25))
                        screen.blit(text3, (coordinate[0], coordinate[1]+50))
                    else:
                        text1 = font.render(building.name, True, black, None)
                        if building.owner == player_1.name:
                            text2 = font.render(player_1.name + str(building.payment * (building.builtRoom + 1)), True, blue, None)
                        elif building.owner == player_com1.name:
                            text2 = font.render(player_com1.name + str(building.payment * (building.builtRoom + 1)), True, red, None)
                        else:
                            text2 = font.render('(無主地)', True, black, None)
                        screen.blit(text1, coordinate)
                        screen.blit(text2, (coordinate[0], coordinate[1]+25))
                font = pygame.font.Font('resource\\font\\tradition.ttf', 30)

            landsNameHP(buildings, MapXYvalue)               
            
                    
            # 印出布告欄與運氣狀態
            board = font.render('**錢幣** 排行榜' , True, black, None)
            money_1 = font.render(player_1.name +'(玩家)錢幣：%d' % player_1.money, True, blue)
            screen.blit(board, (1025, 223))
            screen.blit(money_1, (1033,283))
            
            if player_1.waterUncle == True:
                screen.blit(waterUncle,(1033,313))
            else:
                blit_alpha(screen, waterUncle, (1033,313), half_alpha)
                
            if player_1.moneyLucky == True:
                screen.blit(moneyLucky, (1088,313))
            else:
                blit_alpha(screen, moneyLucky, (1088,313), half_alpha)
            
            if player_1.shuaishen == True:
                screen.blit(shuaishen, (1143,313))
            else:
                blit_alpha(screen, shuaishen, (1143,313), half_alpha)
            
            if player_1.landLucky == True:
                screen.blit(landLucky, (1198,313))
            else:
                blit_alpha(screen, landLucky, (1198,313), half_alpha)
            
        
            money_2 = font.render(player_com1.name +'(電腦)錢幣：%d' % player_com1.money, True, red)
            screen.blit(money_2, (1033,373))        
            if player_com1.waterUncle == True:
                screen.blit(waterUncle, (1033,403))
            else:
                blit_alpha(screen, waterUncle, (1033,403), half_alpha)
        
            if player_com1.moneyLucky == True:
                screen.blit(moneyLucky, (1088,403))
            else:
                blit_alpha(screen, moneyLucky, (1088,403), half_alpha)
            
            if player_com1.shuaishen == True:
                screen.blit(shuaishen, (1143,403))
            else:
                blit_alpha(screen, shuaishen, (1143,403), half_alpha)
                
            if player_com1.landLucky == True:
                screen.blit(landLucky, (1198,403))
            else:
                blit_alpha(screen, landLucky, (1198,403), half_alpha)
                
                
            # 放置扔出来的骰子
            if player_1.dice_value != 0 and showdice:
                screen.blit(dices[player_1.dice_value - 1], (1115, 473))        
            
            # 放置回合结束按紐
            if showButton2:
                screen.blit(turnover2,TurnOvwrButtonPosition)
            else:
                screen.blit(turnover,TurnOvwrButtonPosition)
            
            # 放置是否按钮
            if showYes_No == True:
                screen.blit(yes , YesNoMessageBoxPosition[0])
                screen.blit(no  , YesNoMessageBoxPosition[1])
                
                if showYes2 == True:
                    screen.blit(yes2 , YesNoMessageBoxPosition[0])
                    
                if showNo2 == True:
                    screen.blit(no2 , YesNoMessageBoxPosition[1])
                    
                    
            
                    
            # 印出玩家與電腦位置 
            for i in range(0, 3):
                for each in allplayers:
                    if (each.position == i) and (each == allplayers[0]):
                        screen.blit(each.small_image, MapChessPosition_Player[each.position])
                    elif (each.position == i) and (each == allplayers[1]):
                        screen.blit(each.small_image, MapChessPosition_Com[each.position])
            for i in range(3, 10):
                for each in allplayers:
                    if (each.position == i) and (each == allplayers[0]):
                        x = MapChessPosition_Player[each.position][0]
                        y = MapChessPosition_Player[each.position][1]
                        screen.blit(each.small_image, (x-100, y+100))
                    elif (each.position == i) and (each == allplayers[1]):
                        x = MapChessPosition_Com[each.position][0]
                        y = MapChessPosition_Com[each.position][1]
                        screen.blit(each.small_image, (x-100, y+100))
            for i in range(10, 15):
                for each in allplayers:
                    if (each.position == i) and (each == allplayers[0]):
                        x = MapChessPosition_Player[each.position][0]
                        y = MapChessPosition_Player[each.position][1]
                        screen.blit(each.small_image, (x-10, y+190))
                    elif (each.position == i) and (each == allplayers[1]):
                        x = MapChessPosition_Com[each.position][0]
                        y = MapChessPosition_Com[each.position][1]
                        screen.blit(each.small_image, (x-10, y+190))
            for i in range(15, 22):
                for each in allplayers:
                    if (each.position == i) and (each == allplayers[0]):
                        x = MapChessPosition_Player[each.position][0]
                        y = MapChessPosition_Player[each.position][1]
                        screen.blit(each.small_image, (x+100, y+100))
                    elif (each.position == i) and (each == allplayers[1]):
                        x = MapChessPosition_Com[each.position][0]
                        y = MapChessPosition_Com[each.position][1]
                        screen.blit(each.small_image, (x+100, y+100))
            for i in range(22, 24):
                for each in allplayers:
                    if (each.position == i) and (each == allplayers[0]):
                        screen.blit(each.small_image, MapChessPosition_Player[each.position])
                    elif (each.position == i) and (each == allplayers[1]):
                        screen.blit(each.small_image, MapChessPosition_Com[each.position])
            
            # 輸贏判斷
            for each in allplayers:
                if each.money <= 0:
                    font = pygame.font.Font('resource\\font\\tradition.ttf', 200)
                    loseText1 = font.render(each.name +'輸了!', True, red)
                    loseText2 = font.render('你的系被戰爆了!', True, red)
                    screen.fill(black)
                    screen.blit(loseText1,(100,100))
                    screen.blit(loseText2,(100,300))
                    font = pygame.font.Font('resource\\font\\tradition.ttf',30)            
                    pygame.time.delay(3000)
                        
        
        
        pygame.display.flip()
        clock.tick(60)              
    
            

# 點兩下執行            
if __name__ == "__main__":
    main()            
                                    
                                 

