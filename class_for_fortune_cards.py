import pygame
import random
import sys
class fourtune_card():
    def initiate_cards(self): #製造機會卡的隨機變數
		
		self.cards_value = random.randit(1,7)
       
    def cards_effect(self,position,movavle,credit,money,creditble):

        if self.cards_value == 1:

        	self.creditble = False

        if self.cards_value == 2 :

            if self.money >= 5 :

                self.money -= 5

                self.attack += 1

            else:

                pass

        if cards_value == 3:

            self.movavle = False

        if cards_value == 4:

            total_credit = []
            
            for i in range(0,5):

                total_credit.append(all_players.credit)

            self.crdit += 0.2 * max.total_credit


        if cards_value == 5:

            if self.name != "醫學":
            
                self.movable = False



        if  cards_value == 6:

            if self.name == "醫學":

                self.movable = False

        if cards_value == 7:
            
            if self.money >= 5:

                self.money -= 5

                self.crdit += 3

        return True    






