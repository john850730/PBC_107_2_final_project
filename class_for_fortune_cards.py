import pygame
import random
import sys
class fourtune_card():
    def initiate_cards(self): #製造機會卡的隨機變數
		
		self.cards_value = random.randit(1,7)
       
    def cards_effect(self,position,attack,stars,scores,other_palyers,medic,all_players):

        if self.cards_value == 1:

        	textline1 = self.name + "被當"

        	self.scores += 0

        	self.shohText = [textline1]

        if self.cards_value == 2 :
        

            textline2 = self.name + "出國"

            self.stars -= 5

            self.attack += 1

            self.showText = [textline2]

        if cards_value == 3:

            textline3 = self.name + "吊水源"

            self.position += 0

            self.showText = [textline3]

        if cards_value == 4:
        
            textline4 = self.name + "抱大腿"

            self.stars += 0.2 * max.all_players.stars

            self.showText = [textline4]

        if cards_value == 5:
        
            textline5 = self.name + "舟山路淹水"

            for i in range(0,2):

            	other_palyers.position += 0

            	self.showText = [textline5]

        if  cards_value == 6:

            textline6 = self.name + "凱道誓師大會"

            medic.position += 0

            self.showText = [textline6]

        if cards_value == 7:
            
            textline7 = self.name + "暑修危機分"

            self.stars -= 5

            self.scores += 3

            self.showText = [textline7]

        return True    






