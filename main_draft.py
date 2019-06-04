# -*- coding: utf-8 -*-
"""
NTU Grad Game MainFrame
(Remade version)
"""
import pygame#for all the buttons
import sys#for exit
import random#for dice

# 循環要用的變數      
    running = True#是否循環，遊戲結束才變成False，跳出。
    image_alpha = 255
    button_alpha = 255
    half_alpha = 30
    showdice = True
    showYes2 = False
    showNo2 = False
    showYes_No = False
    pressYes = False
    whetherYes_NoJudge = False
    gameStarted = False#首頁按鍵
    showButton2 = False
    playerCount = 0
    
    
    
###########################################    
if gameStarted:#按了
    screen.blit( backgroud , (0,0) )#切換到遊戲背景圖
    blit_alpha(screen, bigdice_image, (50, 600), image_alpha)#放骰子
            
    textPosition = [MapMessageBoxPosition[0],MapMessageBoxPosition[1]]#放訊息box
    
    #印出訊息
    for each in presentPlayer.showText:
        text = font.render(each, True, white, textColorInMessageBox)
        screen.blit(text,textPosition)
        textPosition[1] += 30
    
    #在每一個地點上，印出血量
    for i in range(1,8):#1,8要看總共幾個建築，8是機會命運牌
        for each in buildings:
            for every in each.location:
                if i == every:
                    if each.owner == allplayers[0]:
                        text = font.render('%d' % (each.HP\
                                                   , True, red)
                    elif each.owner == allplayers[1]:
                        text = font.render('%d' % (each.HP)\
                                                   , True, white)
                    
                    elif each.owner == allplayers[2]:
                        text = font.render('%d' % (each.HP)\
                                                   , True, black)
                    elif each.owner == allplayers[3]:
                        text = font.render('%d' % (each.HP)\
                                                   , True, blue)
                    
                    screen.blit(text,MapChessPosition_Payment[i])
            
            for i in range(9,16):#16是原點
                for each in buildings:
                    for every in each.location:
                        if i == every:
                            if each.owner == allplayers[0]:
                                text = font.render('%d' % (each.HP\
                                                   , True, red)
                        elif each.owner == allplayers[1]:
                            text = font.render('%d' % (each.HP)\
                                                   , True, white)
                    
                        elif each.owner == allplayers[2]:
                            text = font.render('%d' % (each.HP)\
                                                   , True, black)
                        elif each.owner == allplayers[3]:
                            text = font.render('%d' % (each.HP)\
                                                   , True, blue)
                        screen.blit(text,MapChessPosition_Payment[i])                
        
        
    #公佈欄:
    M_1 = font.render(player1.name +'Money：%d' % player1.money, True, black, white)
    C_1 = font.render(player1.name +'Credits：%d/%d' % (player1.credit,player1.graduationCredit), True, black, white)
    M_2 = font.render(player2.name +'Money：%d' % player2.money, True, black, white)
    C_2 = font.render(player2.name +'Credits：%d/%d' % (player2.credit,player2.graduationCredit), True, black, white)
    M_3 = font.render(player3.name +'Money：%d' % player3.money, True, black, white)
    C_3 = font.render(player3.name +'Credits：%d/%d' % (player3.credit,player3.graduationCredit), True, black, white)
    M_4 = font.render(player4.name +'Money：%d' % player4.money, True, black, white)
    C_4 = font.render(player4.name +'Credits：%d/%d' % (player4.credit,player4.graduationCredit), True, black, white)
    
    screen.blit(M_1,(0,0))
    screen.blit(C_1,(0,50))
    screen.blit(M_2,(0,100))
    screen.blit(C_2,(0,150))
    screen.blit(M_3,(0,200))
    screen.blit(C_3,(0,250))
    screen.blit(M_4,(0,300))
    screen.blit(C_4,(0,400))
    
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
                
        
        
        
    #處理按叉叉的事件
    for event in pygame.event.get():
        if event.type == pygame.Quit():
            sys.exit()
    
    #四個玩家要輪流玩，要判斷是換誰    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if bigdice_rect.collidepoint(event.pos):
            presentPlayer = allplayers[playerCount]
            if presentPlayer.movable:
                pygame.time.delay(2000)#故意停一下，假裝骰子在動
                if presentPlayer.name == "哲學":
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
                else:
                    showYes_No = presentPlayer.move(buildings,allplayers)#這一步會丟骰子，並移動地點，並觸發到達目的地後會發生的事件。
                    whetherYes_NoJudge = showYes_No
                    
            else:
                 continue#回去看
        #按回合結束鍵     
        if turnover_rect.collidepoint(event.pos): 
            showButton2 = True#YesNo按鍵True則會出現!
            playerCount += 1
            if playerCount == 4:
                playerCount -= 4  
                          
        else:#什麼都沒按
            showButton2 = False#YesNo按鍵不會出現   
    
    if whetherYes_NoJudge == True:#是否有效 
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
            
    if presentPlayer.buyaBuilding(pressYes) == True:
                pressYes = False
                
            if presentPlayer.addaHouse(pressYes) == True:
                pressYes = False
        
     ##########################################################
 
            
            
    
    
            
            

