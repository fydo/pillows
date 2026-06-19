# Mmmmmm... candies!
# Actually, this is the high-score screen. Woo!

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

class HighScores:

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

    def __init__(self):
        self.headerimg = pygame.image.load(os.path.join('data', 'high-scores.png')).convert_alpha()
        self.part1 = pygame.image.load(os.path.join('data', 'stage.png')).convert()

        self.thefont = pygame.font.Font(os.path.join('data', 'Vera.ttf'), 18)
        self.titlefont = pygame.font.Font(os.path.join('data', 'Vera.ttf'), 23)
        self.scores = self.loadscores()
        
    def blitscores(self, screen, scores):
    
        text = self.titlefont.render("Name", 1, (0,0,0))
        textpos = (120, 120)
        screen.blit(text, textpos)
        
        text = self.titlefont.render("Level", 1, (0,0,0))
        textpos = (375, 120)
        screen.blit(text, textpos)
        
        text = self.titlefont.render("Pillows", 1, (0,0,0))
        textpos = (450, 120)
        screen.blit(text, textpos)
    
        vertoffset = 175
    
        for score, name, pillows  in scores[:5]:
            text = self.thefont.render(name, 1, (0,0,0))
            textpos = (130, vertoffset)
            screen.blit(text, textpos)
            
            text = self.thefont.render(str(score), 1, (0,0,0))
            textpos = (400, vertoffset)
            screen.blit(text, textpos)
            
            text = self.thefont.render(str(pillows), 1, (0,0,0))
            textpos = (480, vertoffset)
            screen.blit(text, textpos)
            
            vertoffset += 50 
        
    def DisplayScores(self, screen):
    
        pygame.time.wait(50)
        
        #fade in 1
        for x in range(15):
            screen.fill((0,0,0))
            work = self.part1
            self.blitscores(work, self.scores)
            work.set_alpha((x * 255) / 15.0, RLEACCEL)
            screen.blit(work, (0,0))
            pygame.display.flip()
            pygame.time.wait(10)
            
        screen.fill((0,0,0))
        screen.blit(self.part1, (0,0))
        self.blitscores(screen, self.scores)
        screen.blit(self.headerimg, (120, 30))
        text = self.thefont.render("Press a button to go to the Main Menu!", 1, (0,0,0))
        textpos = text.get_rect(centerx = screen.get_width()/2, centery = (480 - text.get_height()))
        screen.blit(text, textpos)
        
        pygame.display.flip()
        
        keynotpressed = True
        
        #hold until a key is pressed
        while (keynotpressed):
            pygame.time.wait(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    keynotpressed = False
                elif event.type == JOYBUTTONDOWN:
                    keynotpressed = False
                
        #fade out
        for x in range(50):
            temp = x
            x = 50 - x
            screen.fill((0,0,0))
            work = self.part1
            self.blitscores(work, self.scores)
            work.set_alpha((x * 255) / 50.0, RLEACCEL)
            screen.blit(work, (0,0))
            pygame.display.flip()
            pygame.time.wait(10)
            
        screen.fill((0,0,0))
        pygame.display.flip()
        pygame.time.wait(200)
