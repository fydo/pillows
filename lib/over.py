# Game Over Screen

#-------------------------------------------
#
# pillows - a save-the-world arcade game
#Copyright (C) 2007  fydo  (http://fydo.net)
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#-------------------------------------------

import os, sys
import pygame
from pygame.locals import *

class GameOver:

    def loadscores(self):
        items = []
        
        if os.path.exists(os.path.join(os.path.expanduser("~"), '.pillows-score')):
            file = open(os.path.join(os.path.expanduser("~"), '.pillows-score'), 'r')
        else:
            file = open(os.path.join('data', 'scores.dat'), 'r')
        
        if file:
            for line in file.readlines():
                temp = line.split('\t')
                items.append((int(temp[1].strip()), (temp[0]), (int(temp[2].strip()))))
                
            file.close()
            
        return items
        
    def numeric_compare(self, x, y):
        if x[0]>y[0]:
            return 1
        elif x[0]==y[0]:
            if x[2]<y[2]:
                return 1
            elif x[2]==y[2]:
                return 0;
            else:
                return -1;
        else: # x<y
            return -1

    def savescores(self, items):
        items.sort(self.numeric_compare)
        items.reverse()

        file = open(os.path.join(os.path.expanduser("~"), '.pillows-score'), 'w')

        for score, name, pillows  in items[:5]:
            output = name + "\t" + str(score) + "\t" + str(pillows) + "\n"
            file.write(output)

        file.close()
        
    def __init__(self):
        self.part1 = pygame.image.load(os.path.join('data', 'gameover.png')).convert()
        self.music = pygame.mixer.Sound(os.path.join('data', 'bigboom.ogg'))
        self.thefont = pygame.font.Font(os.path.join('data', 'Vera.ttf'), 18)
        self.titlefont = pygame.font.Font(os.path.join('data', 'Vera.ttf'), 35)
        self.scores = self.loadscores()

    def MoveCharUp(self, char):
        newstuffs = ord(char) + 1
        if newstuffs > 90:
            newstuffs = 65
        return chr(newstuffs)
        
    def MoveCharDown(self, char):
        newstuffs = ord(char) - 1
        if newstuffs < 65:
            newstuffs = 90
        return chr(newstuffs)
        
    def DisplayGameOver(self, screen, noSound, newScore, newPillows):
        
        if (not noSound):
            self.music.play()
        #pygame.time.wait(200)
        
        #fade in 1
        for x in range(15):
            screen.fill((0,0,0))
            work = self.part1
            #self.work.blit(part1, (0,0))
            work.set_alpha((x * 255) / 15.0, RLEACCEL)
            screen.blit(work, (0,0))
            pygame.display.flip()
            pygame.time.wait(10)
            
        
        enteringScore = False
        
        for score, name, pillows  in self.scores[:5]:
            if score < newScore:
                enteringScore = True
        
        if (enteringScore == False):
            showScreen = True
            while (showScreen):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        sys.exit()
                    elif event.type == KEYDOWN:
                        showScreen = False
                    elif event.type == JOYBUTTONDOWN:
                        if (event.button >= 0) and (event.button < 4):
                            showScreen = False
            
                screen.blit(self.part1, (0,0))
                text = self.thefont.render("Sorry, you didn't get a high-score! :(", 1, (0,0,0))
                textpos = ((screen.get_width() - text.get_width())/2, 420)
                screen.blit(text, textpos)
                pygame.display.flip()
                pygame.time.wait(10)
                        
        else:
        
            initials = ["A", "A", "A"]
            currentedit = 0
            allowmove = True
            allowtextmove = True
            MoveUp = False
            MoveDown = False
            MoveAnalog = 0.0
            MoveAnalogDelay = 0.0
            MoveDelay = 0.0
            ElapsedTicks = 0
            LastTicks = 0
            
            while (enteringScore):
            
                thetime = pygame.time.get_ticks()
                ElapsedTicks = thetime - LastTicks
                LastTicks = thetime
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            initials[currentedit] = self.MoveCharUp(initials[currentedit])
                            MoveUp = True
                            MoveDelay = 0.0
                        elif event.key == K_DOWN:
                            initials[currentedit] = self.MoveCharDown(initials[currentedit])
                            MoveDown = True
                            MoveDelay = 0.0                           
                        elif (event.key == K_LEFT):
                            if currentedit > 0:
                                currentedit -= 1
                        elif (event.key == K_RIGHT):
                            if currentedit < 2:
                                currentedit += 1
                        else:
                            checkMe = event.unicode
                            if checkMe.isalpha():
                                initials[currentedit] = checkMe.upper()
                            currentedit += 1
                            if currentedit > 2: 
                                currentedit = 2
                                enteringScore = False
                    elif event.type == KEYUP:
                        if event.key == K_UP:
                            MoveUp = False
                        if event.key == K_DOWN:
                            MoveDown = False
                    elif event.type == JOYBUTTONDOWN:
                        if (event.button >= 0) and (event.button < 4):
                            currentedit += 1
                            if currentedit > 2: 
                                currentedit = 2
                                enteringScore = False
                    elif event.type == JOYHATMOTION:
                        if ((event.value[1] < -0.1)): #(event.hat == 1) and
                            initials[currentedit] = self.MoveCharDown(initials[currentedit])
                            MoveDown = True
                            MoveDelay = 0.0    
                        elif ((event.value[1] > 0.1)):
                            initials[currentedit] = self.MoveCharUp(initials[currentedit])
                            MoveUp = True
                            MoveDelay = 0.0
                        elif ((event.value[1] > -0.1) and (event.value[1] < 0.1)):
                            MoveUp = False
                            MoveDown = False
                        elif ((event.value[0] < -0.1)):
                            if currentedit > 0:
                                currentedit -= 1
                        elif ((event.value[0] > 0.1)):      
                            if currentedit < 2:
                                currentedit += 1
                    elif event.type == JOYAXISMOTION:
                        if ((event.axis == 1)):# and (event.value < -0.5)): # and allowtextmove):
                            MoveAnalog = event.value
                            MoveAnalogDelay = -((1.1 - abs(MoveAnalog)) - 0.5) * 150
                        elif ((event.axis == 0) and (event.value < -0.5)):
                            if currentedit > 0 and allowmove:
                                currentedit -= 1
                                allowmove = False
                        elif ((event.axis == 0) and (event.value > 0.5)):
                            if currentedit < 2 and allowmove:
                                currentedit += 1
                                allowmove = False
                        elif ((event.axis == 0) and (event.value < 0.5) and (event.value > -0.5)):
                                allowmove = True
                        #elif ((event.axis == 1) and (event.value < 0.5) and (event.value > -0.5)):
                                #allowtextmove = True
                
                if MoveUp or MoveDown or (MoveAnalog > 0.1) or (MoveAnalog < -0.1):
                
                    MoveDelay += ElapsedTicks
                    
                    if (MoveDelay + MoveAnalogDelay) > 180:
                        MoveDelay = 0.0
                        
                        if MoveUp:
                            initials[currentedit] = self.MoveCharUp(initials[currentedit])
                        elif MoveDown:
                            initials[currentedit] = self.MoveCharDown(initials[currentedit]) 
                        elif MoveAnalog > 0.1:
                            initials[currentedit] = self.MoveCharDown(initials[currentedit]) 
                        elif MoveAnalog < -0.1:
                            initials[currentedit] = self.MoveCharUp(initials[currentedit])
                            
                
                screen.blit(self.part1, (0,0))                        
                
                text = self.thefont.render("You got a high score! Enter your name:", 1, (0,0,0))
                textpos = ((screen.get_width() - text.get_width())/2, 390)
                screen.blit(text, textpos)
                
                text = self.titlefont.render(initials[0], 1, (0,0,0))
                textpos = (260, 417)
                screen.blit(text, textpos)
                
                text = self.titlefont.render("_", 1, (0,0,0))
                textpos = (260, 420)
                screen.blit(text, textpos)
                
                text = self.titlefont.render(initials[1], 1, (0,0,0))
                textpos = (310, 417)
                screen.blit(text, textpos)
                
                text = self.titlefont.render("_", 1, (0,0,0))
                textpos = (310, 420)
                screen.blit(text, textpos)
                
                text = self.titlefont.render(initials[2], 1, (0,0,0))
                textpos = (360, 417)
                screen.blit(text, textpos)
                
                text = self.titlefont.render("_", 1, (0,0,0))
                textpos = (360, 420)
                screen.blit(text, textpos)
                
                #selector helper thingy
                text = self.titlefont.render("^", 1, (100,100,100))
                textpos = (256 + (currentedit * 49), 460)
                screen.blit(text, textpos)
                
                pygame.display.flip()
                pygame.time.wait(15)
                
            self.scores.append((newScore, initials[0] + initials[1] + initials[2], newPillows))
            self.savescores(self.scores)
            
        #pygame.time.wait(2600) #tweak me.. oh yeah
                
        #fade out
        for x in range(50):
            temp = x
            x = 50 - x
            screen.fill((0,0,0))
            work = self.part1
            work.set_alpha((x * 255) / 50.0, RLEACCEL)
            screen.blit(work, (0,0))
            pygame.display.flip()
            pygame.time.wait(10)
            
        screen.fill((0,0,0))
        pygame.display.flip()
        pygame.time.wait(100)
