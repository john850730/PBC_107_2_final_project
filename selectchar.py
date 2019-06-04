 # 循环开始！ 
    while running:
        if not gameStarted:
			if not Selectcharatcer
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
							
					if event.type == pygame.MOUSEBUTTONDOWN:
						 
						if button_start.collidepoint(event.pos): # 按下按钮
							didong.play()                     
							Selectcharatcer = True  
				screen.blit(GameStart , (0,0))       
				blit_alpha(screen, StartGameButton, StartGameButtonPosition, button_alpha)
			
			
			if Selectcharatcer:				 
				allset = 0
				selected = []
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if button_player1.collidepoint(event.pos) and allset == 0: # 按下按钮            
					    ismajor = random.randint(0,9)
						for i in range(len(majorlist)):
							if i==ismajor:
								name1 = majorlist[i]
								selected.append(i)
						allset+=1
						
					
					if button_player2.collidepoint(event.pos) and allset == 1: # 按下按钮            
					    ismajor = random.randit(0,9)
						while ismajor in selected:
							ismajor = random.randit(0,9)
						
						for i in range(len(majorlist)):
							if i==ismajor:
								name2 = majorlist[i]
								selected.append(i)
						allset +=1
					
					if button_player3.collidepoint(event.pos) and allset == 2: # 按下按钮            
					    ismajor = random.randit(0,9)
						while ismajor in selected:
							ismajor = random.randit(0,9)
						
						for i in range(len(majorlist)):
							if i==ismajor:
								name3 = majorlist[i]
								selected.append(i)
						allset +=1
						
					if button_player4.collidepoint(event.pos) and allset ==3: # 按下按钮            
					    ismajor = random.randit(0,9)
						while ismajor in selected:
							ismajor = random.randit(0,9)
						
						for i in range(len(majorlist)):
							if i==ismajor:
								name4 = majorlist[i]
								selected.append(i)
						allset +=1
					
				if allset ==4:
					GameStart = True

				screen.blit(GameStart , (0,0))       
				blit_alpha(screen,selectacharacterbtn, ButtonPosition, button_alpha)
				#等一下要設定
				#然後也要把每個角色的圖片跟選擇鍵設定好