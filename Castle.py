# -*- coding: utf-8 -*-
"""
本Castle class將取代原程式的 "Building" class
當玩家按YES鍵，會創造屬於那個地點的 "Castle" Object

Castle class 分為等級一(只有土地) 與 等級二(有建築)
變數:
    level: 等級 (1:土地 ==> 2:建築)
    name: 地名 
    owner: 擁有者 (預設:none, 當被買走或被打敗後，用player_name進行取代)
    price: 價位 (要買下這裡需要多少星星)
    stars: 星星數(每回合送的星星數)
    HP: 血量 (被別人攻擊後，會減少)
    credit: 學分
    location: 地點 (為了辨別這個建築在那裡用)
    wasBrought: 是否被買下(預設False)
    toll: 過路費
    
函式:
    calculateScore(): 計算
    
    
    
城堡Class:
1.興建:
    當角色到達一塊土地時，可以用星星購買此土地。(class player)
    再次到達時，可以用星星興建一座城堡。(class player)
    每個土地/城堡的價位(星星數)不同。self.price
2.城堡有HP:
    每個城堡有一個血量，原則上只增不減。
    別人到達你的城堡，可以發動攻擊，減少你的城堡HP。(class player?!)
3.每一回合結束:
    每座城堡可以獲得某個特定數量的積分與星星。
    要把每個玩家擁有的總城堡數、積分數、星星數統整。(輸出給公布欄)
    
"""
import pygame

class Castle():
    def __init__(self, level, name, owner, price, stars, HP,loss_amt, credit, location, wasBrought, toll):
        self.level = 1
        self.name = name
        self.owner = owner
        self.price = price
        self.stars = stars
        self.HP = HP
        self.loss_amt = 0
        self.credit = credit
        self.location = location
        self.wasBought = False
        self.owner = "none"
        self.toll = toll
        self.icon = pygame.image.load("要加城堡的圖")
        
    #在Player裡，會有一個功能計算每回合結束，該玩家有多少資產(countAssets)與該輪
    
    def CastleDestroyed(self, Player):#打敗此城堡的玩家物件
        self.owner = Player.name#取而代之
        self.HP += self.loss_amt#怎麼變回原本的HP?!
        

