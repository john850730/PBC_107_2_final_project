# -*- coding: utf-8 -*-


#  code by:  物网141 王璞劼Khalil
#  name:     理工大富翁beta2.0
#  describe: 基于python的一个2D大富翁游戏
'''
1.游戏地图为自己使用各种网络素材制作；
  各种按钮和选项，小图标等也是使用PS制作。

2.声音效果主要为背景音乐和几种游戏中音效；

3.游戏设定了两个类：玩家和建筑
  玩家的参数和方法都在代码中给出；
  具体有：移动方法、位置判断方法、
  	 购买房屋方法、添加小房子方法、
	 事件判断方法。

4.玩家在大富翁的主要操作是投掷骰子，由随机函数
  进行判定然后进行移动，进行位置判断，然后开始
  进行相关的判定。

5.游戏中的按键有：是、否、和结束回合；
  每个按键由没按下与按下两种状态的图片组成，
  这个设计花费了一定时间。
  还有 开始游戏 和 扔骰子 的两个明暗按钮，
  由pygame优化后的一个函数实现。

6.玩家的位置与电脑重叠时会将双方的位置进行一定
  偏移，防止进行覆盖，分不清自己的位置。

7.游戏基础功能有移动，购买房子，在已经购买的房子下
  搭建新的小房子增加过路费，被收费，判断胜负的基础
  功能，此外还加入了幸运事件：
    财神 - 免收费一次
    衰神 - 双倍被收费一次
    破坏神 - 直接破坏一个建筑 无论敌我
    土地神 - 强占对面建筑
  这四项功能在位置处于左上角和右下角的时候会被触发，
  添加了很多游戏乐趣哦~~~ ^_^

8.游戏基于python的一个模块pygame实现，给我提供了很
  多快乐的时光，谢谢老师的阅览与郭宁同学的协助答辩
  ：）
'''

########################################准备工作###############################################

# 初始化各种模块
import pygame
import random
import sys

# 定义类
class Player():
    def __init__(self, image ,name , isPlayer):
        self.name = name
        self.money = 10000
        self.isGoingToMove = False 
        self.movable = True
        self.image = image
        self.position = 0  
        self.temp_position = False
        self.dice_value = 0
        self.locatedBuilding = 0
        self.showText = []
        self.isPlayer = isPlayer#自己??
        self.ownedBuildings = []
        self.isShowText = False
        self.soundPlayList = 0
        self.caishen = 0
        self.shuaishen = 0
        self.tudishen = 0
        self.pohuaishen = 0
        
    #位置判断 返回值是所在位置的建筑
    def judgePosition(self,buildings): #buildings is a list of the Building Objects we created
        for each in buildings:#"each" is a object of class building
            for every in each.location:#get the location of the building
                if self.position == every:#find where we are located right now
                    return each
                    
            
            # 当使用元组时 当元组中只有一个元素时 发现该元素不可迭代 
            # 出现错误 换成列表后解决
            ''' 
            try:
                for every in each.location:
                    if self.position == every:
                        print(each.name)
            except:
                if self.position == every:
                    print(each.name)
            '''
            
    def buyaBuilding(self,isPressYes):    # 购买方法
        if isPressYes and self.locatedBuilding.owner != self.name:#有按yes，然後不適自己的
            self.locatedBuilding.owner = self.name
            self.locatedBuilding.wasBought = True
            self.ownedBuildings.append(self.locatedBuilding)
            self.money -= self.locatedBuilding.price
            self.showText = [self.name + '购买了' + self.locatedBuilding.name + '!']
            self.soundPlayList = 1
            return True
        else:
            return False
        
          
            
    def addaHouse(self,isPressYes): # 在建筑物上添加一个房子
        try:
            if isPressYes and self.locatedBuilding.owner == self.name:
                self.locatedBuilding.builtRoom += 1
                self.money -= self.locatedBuilding.payment
                self.showText = [self.name + '在' + self.locatedBuilding.name + '上!','盖了一座房子！',\
                                '有%d' % self.locatedBuilding.builtRoom + '个房子了！',\
                                "它的过路费是%d" % (self.locatedBuilding.payment * \
                                                (self.locatedBuilding.builtRoom + 1)) ]
                self.soundPlayList = 2
                return True
            else:
                return False
        except:
            pass
    
    def move(self,buildings,allplayers):   # 移动方法 返回值是所在的建筑位置
        self.dice_value =  random.randint(1,6)
        self.position += self.dice_value
        if self.position >= 16:
            self.position -= 16
        self.locatedBuilding = self.judgePosition(buildings)
        self.isShowText = True
        return self.eventInPosition(allplayers)
    
    
    def eventInPosition(self,allplayers):        # 判断在建筑位置应该发生的事件        
        building = self.locatedBuilding
        if building.name != '空地':
            if self.locatedBuilding.wasBought == False: # 未购买的时候显示建筑的数据！(無主地)
                if self.isPlayer == True:
                    textLine0 = self.name +'扔出了' + '%d'% self.dice_value + '点！'
                    textLine1 = self.name +'来到了' + building.name + '!'
                    textLine2 = '购买价格：%d' % building.price
                    textLine3 = '过路收费：%d' % building.payment
                    textLine4 = '是否购买？'
                    self.showText = [textLine0,textLine1,textLine2,textLine3,textLine4]
                    return True
                else :
                    self.addaHouse(not self.buyaBuilding(True))
                    
                # ----- 动画 -------
                # ----- 是否购买 ------
            elif building.owner == self.name: # 路过自己的房子开始加盖建筑！
                if self.pohuaishen == 1:
                    textLine0 = self.name + '破坏神附体！'
                    textLine1 = '摧毁了自己的房子！'
                    building.owner = 'no'
                    building.wasBought = False
                    self.showText = [textLine0,textLine1]
                    self.pohuaishen = 0
                else:
                    if self.isPlayer == True:
                        textLine0 = self.name + '扔出了' + '%d'% self.dice_value + '点！'
                        textLine1 = '来到了ta的'+ self.locatedBuilding.name +'!'
                        textLine2 = '可以加盖小房子！' 
                        textLine3 = '加盖收费：%d' % building.payment
                        textLine4 = '是否加盖？'
                        self.showText = [textLine0,textLine1,textLine2,textLine3,textLine4]
                        return True
                    # ----- 动画-------
                    else:
                        self.addaHouse(True)
            else:
                for each in allplayers: # 被收费！
                    if self.locatedBuilding.owner == each.name and each.name != self.name:
                        if self.caishen == 1:
                            textLine0 = self.name + '财神附体！'
                            textLine1 = '免除过路费%d！' % (building.payment * (building.builtRoom + 1))
                            self.showText = [textLine0,textLine1]
                            self.caishen = 0
                        else:
                            if self.tudishen == 1:
                                textLine0 = self.name + '土地神附体！'
                                textLine1 = '强占土地！'
                                textLine2 = building.name + '现在属于'+ self.name
                                self.locatedBuilding.owner = self.name
                                self.showText = [textLine0,textLine1,textLine2]
                                self.tudishen = 0
                            else:
                                if self.pohuaishen == 1:
                                    textLine0 = self.name + '破坏神附体！'
                                    textLine1 = '摧毁了对手的房子！'
                                    building.owner = 'no'
                                    building.wasBought = False
                                    self.
				
				showText = [textLine0,textLine1]
                                    self.pohuaishen = 0   
                                else:
                                    textLine0 = self.name + '扔出了' + '%d'% self.dice_value + '点！'
                                    textLine1 = self.name+ '来到了'+ each.name+'的:'  
                                    textLine2 = building.name + '，被收费!'
                                    if self.shuaishen == 1:
                                        textLine3 = '过路收费：%d*2!' % (building.payment * (building.builtRoom + 1)*2)
                                        self.shuaishen = 0
                                    else:
                                        textLine3 = '过路收费：%d' % (building.payment * (building.builtRoom + 1))
                                    textLine4 = '哦！'+ self.name +'好倒霉！'
                                    self.showText = [textLine0,textLine1,textLine2,textLine3,textLine4]
                                    # 收费！
                                    self.money -= building.payment * (building.builtRoom + 1)
                                    each.money += building.payment * (building.builtRoom + 1)
                                    self.soundPlayList = 3
                                    # ----- 动画-------
                        
        else:#是空地(沒有建築)
            # 发现不能处理在空地上的情况 于是使用 try & except 来解决！然后加入了幸运事件功能！
            # 后来发现 try except 弊端太大 找不到错误的根源 换为if else嵌套。。
            whichone = self.dice_value % 4
            if whichone == 0:
                self.caishen = 1
                textLine2 = '遇到了财神！'
                textLine3 = '免一次过路费！'
            if whichone == 1:
                self.shuaishen = 1
                textLine2 = '遇到了衰神！'
                textLine3 = '过路费加倍一次！'
            if whichone == 2:
                self.tudishen = 1
                textLine2 = '遇到了土地神！'
                textLine3 = '强占一次房子！'
            if whichone == 3:
                self.pohuaishen = 1
                textLine3 = '摧毁路过的房子！'
                textLine2 = '遇到了破坏神！'
            textLine0 = self.name +'扔出了' +'%d'% self.dice_value + '点！'
            textLine1 = '来到了运气地点！'
            self.showText = [textLine0,textLine1,textLine2,textLine3]

    
    
    
class Building():                           # 好像所有功能都在Player类里实现了=_=
    def __init__(self,name,price,payment,location):
        self.name = name
        self.price = price
        self.payment = payment
        self.location = location
        self.wasBought = False               # 是否被购买
        self.builtRoom = 0                   # 小房子建造的数目
        self.owner = 'no'
    
    


# 带透明度的绘图方法 by turtle 2333
def blit_alpha(target,source,location,opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(),source.get_height())).convert()
    temp.blit(target , (-x , -y))
    temp.blit(source,(0,0))
    temp.set_alpha(opacity)
    target.blit(temp,location)




########################################主函数###############################################    


def main():
    pygame.init()#initialize all modules(import 所有東西)
    clock = pygame.time.Clock()#create an object to help track time(?)
    
    # 初始化螢幕
    size = (1270,768)
    screen = pygame.display.set_mode(size)#Initialize a window or screen for display, parameter 是大小
    pygame.display.set_caption("PBC 2019 SPRING: 誰能先畢業?")#title
    
    # 設定字體與字顏色
    textColorInMessageBox = (141,146,152)#這三個數字決定顏色，然後存入變數
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    font = pygame.font.Font('resource\\font\\myfont.ttf',30)#創建字體對象
    
    
    # 從電腦讀取圖片 load new image from a file, works with png, jpg, GIF
    backgroud = pygame.image.load("resource\\pic\\GameMap.png")#resource是個資料夾，他跟遊戲py檔在同一個資料夾裡
    chess = pygame.image.load("resource\\pic\\chess.png")
    chess_com =  pygame.image.load("resource\\pic\\chess1.png")
    bigdice_image = pygame.image.load("resource\\pic\\dice.png").convert_alpha()#use the convert_alpha() method after loading so that the image has per pixel transparency.
    dice_1 = pygame.image.load("resource\\pic\\dice_1.png")
    dice_2 = pygame.image.load("resource\\pic\\dice_2.png")
    dice_3 = pygame.image.load("resource\\pic\\dice_3.png")
    dice_4 = pygame.image.load("resource\\pic\\dice_4.png")
    dice_5 = pygame.image.load("resource\\pic\\dice_5.png")
    dice_6 = pygame.image.load("resource\\pic\\dice_6.png")
    dices = [dice_1,dice_2,dice_3,dice_4,dice_5,dice_6]#骰子投完後，會將結果輸出到介面，讓玩家看
    yes = pygame.image.load("resource\\pic\\yes.png")#"Yes" button
    yes2 = pygame.image.load("resource\\pic\\yes2.png")
    no = pygame.image.load("resource\\pic\\no.png")
    no2 = pygame.image.load("resource\\pic\\no2.png")
	
    GameStart = pygame.image.load("resource\\pic\\GameStart.png")#開始頁面
    StartGameButton = pygame.image.load("resource\\pic\\StartGameButton.png").convert_alpha()
    turnover = pygame.image.load("resource\\pic\\turnover.png")
    turnover2 = pygame.image.load("resource\\pic\\turnover2.png")
   
    #以下是他們遊戲裡的四個神明，我們用不到
    shuaishen = pygame.image.load("resource\\pic\\shuaishen.png").convert_alpha()
    tudishen = pygame.image.load("resource\\pic\\tudishen.png").convert_alpha()
    caishen = pygame.image.load("resource\\pic\\caishen.png").convert_alpha()
    pohuaishen = pygame.image.load("resource\\pic\\pohuaishen.png").convert_alpha()
    
    #上音效
    rollDiceSound = pygame.mixer.Sound("resource\\sound\\rolldicesound.wav")#我們可以考慮加一點點音效(娛樂效果)，如校歌
    bgm = pygame.mixer.music.load("resource\\sound\\bgm.ogg")
    throwcoin = pygame.mixer.Sound("resource\\sound\\throwcoin.wav")
    moneysound = pygame.mixer.Sound("resource\\sound\\moneysound.wav")
    aiyo = pygame.mixer.Sound("resource\\sound\\aiyo.wav")
    didong = pygame.mixer.Sound("resource\\sound\\didong.wav")
    
    # PlayList 在對象中，設置應撥放的聲音
    playList = [moneysound ,throwcoin ,aiyo]
    
    # 在畫布上，畫出該出現的各種東西，然後設定它們的位置 
    bigdice_rect = bigdice_image.get_rect()#在畫布上畫出來這個圖，且規定他是矩形的
    bigdice_rect.left , bigdice_rect.top = 50 , 600#設定它的位置

    yes_rect = yes.get_rect()
    yes_rect.left , yes_rect.top = 500,438 
    
    no_rect = no.get_rect()
    no_rect.left , no_rect.top =  630,438
    button_rect = StartGameButton.get_rect()
    button_rect.left , button_rect.top = 1003,30
    turnover_rect = turnover.get_rect()
    turnover_rect.left , turnover_rect.top = 1035,613
    
    # 初始化玩家，他們的遊戲只有單機版，自己打電腦而已
    players = []#放所有玩家
    computers = []#他們有AI
    allplayers = []
    player_1 = Player(chess , '玩家' , True )#產生一個玩家物件
    player_com1 = Player(chess_com , '电脑' , False )
    players.append(player_1)
    computers.append(player_com1)
    allplayers.append(player_1)
    allplayers.append(player_com1)
    
    presentPlayer = player_com1
    
    # 初始化建築(我們是用Castle Class)
    gate = Building('大门',1000,200,[1,2])#self,name,price,payment,location(?)
    fountain = Building('喷泉',2000,400,[3,4])
    path = Building('小道',800,160,[5])
    library = Building('图书馆',2000,400,[6,7])
    kongdi1 = Building('空地',0,0,[8])
    classroomTen = Building('教十',1200,240,[9,10])
    classroomNine = Building('教九',1200,240,[11,12])
    resOne = Building('三餐厅',800,160,[13])
    resTwo = Building('二餐厅',800,160,[14])
    resThree = Building('一餐厅',800,160,[15])
    kongdi2 = Building('空地',0,0,[0])#有點笨，不應該讓兩個地方名字一樣!
    
    buildings = [gate,fountain,path,library,classroomNine,\
                 classroomTen,resOne,resThree,resTwo,kongdi1,kongdi2]
    
    
    
    # 裝好所有座標的list，共有16個座標
    MapXYvalue = [(435.5,231.5),(509.5,231.5),(588.5,231.5),(675.5,231.5),(758.5,231.5),\
                  (758.5,317.0),(758.5,405.5),(758.5,484.5),(758.5,558.5),(679.5,558.5),\
                  (601.5,558.5),(518.5,556.5),(435.5,556.5),(435.5,479.5),(435.5,399.0),\
                  (435.5,315.5)
                  ]
    
    MapChessPosition_Player = []#紀錄玩家位置?
    MapChessPosition_Com = []
    MapChessPosition_Original = []#紀錄甚麼位置??
    MapChessPosition_Payment = []#紀錄甚麼位置???
    
    #設定介面各個東西的位置
    MapMessageBoxPosition = (474.1 , 276.9)
    YesNoMessageBoxPosition = [(500,438) , (630,438)]#為甚麼是list
    StartGameButtonPosition = (1003,30)
    TurnOvwrButtonPosition = (1035,613)
    
    
    # 調整位置(?!!為何，這一步在幹麻?還是只是看著錶調整)
    for i in range(0,16):
        MapChessPosition_Original.append((MapXYvalue[i][0]-50,MapXYvalue[i][1]-80))
        MapChessPosition_Player.append((MapXYvalue[i][0]-70,MapXYvalue[i][1]-60))
        MapChessPosition_Com.append((MapXYvalue[i][0]-30,MapXYvalue[i][1]-100))
        MapChessPosition_Payment.append((MapXYvalue[i][0]-30,MapXYvalue[i][1]-15))
    
    
    
        
    
    # 循環要用的變數      
    running = True#是否循環，遊戲結束才變成False，跳出。
    image_alpha = 255#(?what is alpha)
    button_alpha = 255#(?)
    half_alpha = 30#(?)
    showdice = True
    showYes2 = False
    showNo2 = False
    showYes_No = False
    pressYes = False
    whetherYes_NoJudge = False
    gameStarted = False#首頁按鍵
    showButton2 = False
    
    # 播放背景音樂(我們不要)
    pygame.mixer.music.play(100)
    
########################################进入游戏循环！###############################################    


    # 循環開始！ 
    while running:#running預設是True
        if not gameStarted:#gameStarted預設False
            for event in pygame.event.get():#在循環中，會不斷蒐集發生事件的發生
                if event.type == pygame.QUIT:#QUIT是指把視窗關掉!
                    sys.exit()
                
                # 滑鼠點到，明暗改變
                if event.type == pygame.MOUSEMOTION:#MOUSEMOTION好像會紀錄滑鼠的動作
                    if button_rect.collidepoint(event.pos):#collidepoint會去確認()裡的點，是否在一個矩形裡，return True。Pos會回傳位置
                        button_alpha = 255#如果點到button，顏色改變   
                    else:
                        button_alpha = 120#沒有點到，改變 
                # 滑鼠點到，        
                if event.type == pygame.MOUSEBUTTONDOWN:#MOUSEBUTTONDOWN按下去的意思
                     
                    if button_rect.collidepoint(event.pos): # 按的點在框框內
                        didong.play()#撥放音樂                    
                        gameStarted = True#遊戲正式開始  
            
            screen.blit(GameStart , (0,0))#blit: draw one image onto another，換成GameStart，(0,0)應該是位置
            blit_alpha(screen, StartGameButton, StartGameButtonPosition, button_alpha)
        
        
        
        if gameStarted:#剛剛按了後，變成True
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                # 滑鼠在它上面，有明暗變化
                if event.type == pygame.MOUSEMOTION:
                    if bigdice_rect.collidepoint(event.pos):
                        image_alpha = 255   
                    else:
                        image_alpha = 190
                        
                
                if event.type == pygame.MOUSEBUTTONDOWN:#滑鼠有點下去
                    #muliple player這裡要重新設計!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    if bigdice_rect.collidepoint(event.pos): # 按骰子按鍵
                        if presentPlayer != player_1:#預設presentPlayer == player_com，所以這個一開始一定跑!之後presentPlayer都是輪的玩家。
                            rollDiceSound.play(1, 2000)
                            pygame.time.delay(2000)#故意停一下，假裝骰子在動
                            showYes_No = player_1.move(buildings,allplayers)#這一步會丟骰子，並移動地點，並觸發到達目的地後會發生的事件。
                            whetherYes_NoJudge = showYes_No#whetherYes_NoJudge預設是False，return可能會是True也能是False，要看情況
                            presentPlayer = player_1#換人，換成player1
                        else:
                            presentPlayer.showText = ['还没到你的回合！']
                        
                    if turnover_rect.collidepoint(event.pos): # 按回合结束
                        showButton2 = True#YesNo按鍵True則會出現!
                        if presentPlayer != player_com1:#同裡，presentPlayer是前一輪的玩家
                            showYes_No = player_com1.move(buildings,allplayers)#骰子==> 移動 ==> 效果
                            presentPlayer = player_com1
                        else:
                            presentPlayer.showText = ['还没到你的回合！']                            
                    else:#什麼都沒按
                        showButton2 = False
                    
                        # 不显示Yes_No的时候不能点击它们！
                    if whetherYes_NoJudge == True: 
                        if yes_rect.collidepoint(event.pos): # 按Yes
                            showYes2 = True
                            
                        if no_rect.collidepoint(event.pos): # 按No
                            showNo2  = True
                      
                if event.type == pygame.MOUSEBUTTONUP:#Up vs down?!
                    
                    if turnover_rect.collidepoint(event.pos): # 按回合结束
                        showButton2 = False
                    
                    if yes_rect.collidepoint(event.pos): # 按是否
                        showYes2 = False#1 or 2 只是表示按鍵突出還是往下
                        showYes_No = False
                        # 只有在可以判定的时候才能算按下了是 同时将判断条件置为空
                        if whetherYes_NoJudge == True:
                            pressYes = True#才算是
                            whetherYes_NoJudge = False#重新
                            
                            
                    if no_rect.collidepoint(event.pos): # 按是否
                        showNo2 = False
                        pressYes = False
                        showYes_No = False              
                        whetherYes_NoJudge = False        
            
                # 外掛:        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:#按w，玩家一值動
                        showYes_No = player_1.move(buildings,allplayers)
                        whetherYes_NoJudge = showYes_No
                        presentPlayer = player_1
                    if event.key == pygame.K_q:#按q電腦一值動
                        showYes_No = player_com1.move(buildings,allplayers)
                        presentPlayer = player_com1
            
            
            '''for each in allplayers:
                if each.isGoingToMove == True and each.movable == True :
                    showYes_No = each.move(buildings,allplayers)
                    each.movable = False
                    each.isGoingToMove = False'''
            '''
            allisready = True
            
            for each in allplayers:
                if each.movable == True:
                    allisready = False
            
            if allisready:
                for each in allplayers:
                    each.movable = True
            ''' 
            
            
            
                
             
            # 购买房屋！！！！！！！！
            
            if presentPlayer.buyaBuilding(pressYes) == True:
                pressYes = False
                
            if presentPlayer.addaHouse(pressYes) == True:
                pressYes = False
            
                
            
                
                    
                
            #########################################################################            
            screen.blit( backgroud , (0,0) )
            blit_alpha(screen, bigdice_image, (50, 600), image_alpha)
            
            
            textPosition = [MapMessageBoxPosition[0],MapMessageBoxPosition[1]]
            
            # 打印信息
            for each in presentPlayer.showText:
                text = font.render(each, True, white, textColorInMessageBox)
                screen.blit(text,textPosition)
                textPosition[1] += 30
            
            # 播放行动声音
            if presentPlayer.soundPlayList != 0:
                playList[presentPlayer.soundPlayList - 1].play()
                presentPlayer.soundPlayList = 0
                
            # 在位置上显示过路费
            
            for i in range(1,8):
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == presentPlayer.name:
                                text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                   , True, red)
                            elif each.owner == 'no':
                                text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                   , True, white)
                            elif each.owner != presentPlayer.name and each.owner != 'no':
                                text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                   , True, black)
                            screen.blit(text,MapChessPosition_Payment[i])
            
            for i in range(9,16):
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == presentPlayer.name:
                                text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                   , True, red)
                            elif each.owner == 'no':
                                text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                   , True, white)
                            elif each.owner != presentPlayer.name and each.owner != 'no':
                                text = font.render('%d' % (each.payment * (each.builtRoom + 1))\
                                                   , True, black)
                            screen.blit(text,MapChessPosition_Payment[i])                
            
                    
            # 打印金钱数和幸运状态  明展!!!!這裡要改成狀態!!
            
            money_1 = font.render(player_1.name +'金钱：%d' % player_1.money, True, black, white)
            screen.blit(money_1,(0,0))
            
            if player_1.pohuaishen == True:
                screen.blit(pohuaishen,(0,30))
            else:
                blit_alpha(screen, pohuaishen, (0, 30), half_alpha)
                
            if player_1.caishen == True:
                screen.blit(caishen,(55,30))
            else:
                blit_alpha(screen, caishen, (55, 30), half_alpha)
            
            if player_1.shuaishen == True:
                screen.blit(shuaishen,(110,30))
            else:
                blit_alpha(screen, shuaishen, (110, 30), half_alpha)
            
            if player_1.tudishen == True:
                screen.blit(tudishen,(165,30))
            else:
                blit_alpha(screen, tudishen, (165, 30), half_alpha)
            
        
            money_2 = font.render(player_com1.name +'金钱：%d' % player_com1.money, True, black, white)
            screen.blit(money_2,(1000,0))        
            if player_com1.pohuaishen == True:
                screen.blit(pohuaishen,(1000,30))
            else:
                blit_alpha(screen, pohuaishen, (1000, 30), half_alpha)
        
            if player_com1.caishen == True:
                screen.blit(caishen,(1055,30))
            else:
                blit_alpha(screen, caishen, (1055, 30), half_alpha)
            
            if player_com1.shuaishen == True:
                screen.blit(shuaishen,(1110,30))
            else:
                blit_alpha(screen, shuaishen, (1110, 30), half_alpha)
                
            if player_com1.tudishen == True:
                screen.blit(tudishen,(1165,30))
            else:
                blit_alpha(screen, tudishen, (1165, 30), half_alpha)
                
                
            # 放置扔出来的骰子
            if player_1.dice_value != 0 and showdice:
                screen.blit(dices[player_1.dice_value - 1],(70,450))        
            
            # 放置回合结束按钮
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
                    
                    
            
                    
                    
            # 放置玩家与电脑的位置 如果重合则挪位
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
                
            
            
            # 输赢判断: 要重寫
            for each in allplayers:
                if each.money <= 0:
                    font = pygame.font.Font('resource\\font\\myfont.ttf',200)
                    loseText = font.render(each.name +'输了！', True, red)
                    screen.fill(black)
                    screen.blit(loseText,(100,100))
                    font = pygame.font.Font('resource\\font\\myfont.ttf',30)            
                    pygame.time.delay(3000)
                        
        # 画面运行
        
        pygame.display.flip()
        clock.tick(60)              # 刷新率
    
            

# 双击打开运行            
if __name__ == "__main__":
    main()            
                                    
                                 




