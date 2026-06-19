# Main menu for the game 

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

class Menu:
    def __init__(self):
        #load stuff
        self.bgimage = pygame.image.load(os.path.join('data', 'menu.png')).convert()
        self.selectimage = pygame.image.load(os.path.join('data', 'select.png')).convert_alpha()
        self.movesound = pygame.mixer.Sound(os.path.join('data', 'menu.ogg'))
        self.selsound = pygame.mixer.Sound(os.path.join('data', 'menuselect.ogg'))
        self.selection = 0
            
    def PickIt(self, screen):
        #FANCY FADE OUT!
        for x in range(50):
            temp = x
            x = 50 - x
            screen.fill((0,0,0))
            work = self.bgimage
            work.set_alpha((x * 255) / 50.0, RLEACCEL)
            screen.blit(work, (0,0))
            pygame.display.flip()
            pygame.time.wait(10)
        
        return self.selection
        
    def MoveDown(self, screen):
        if self.selection == 3:
            return
        self.movesound.play()
        temploc = 233 + (self.selection * 48)
        yvel = 0
        self.selection += 1
        while (temploc < (233 + (self.selection * 48))):
            yvel += 1
            screen.blit(self.bgimage, (0,0))
            temploc += yvel
            selectloc = (356,temploc)
            screen.blit(self.selectimage, selectloc)
            pygame.display.flip()
            pygame.time.wait(15)
        
            
    def MoveUp(self, screen):
        if self.selection == 0:
            return
        self.movesound.play()
        temploc = 233 + (self.selection * 48)
        yvel = 0
        self.selection -= 1
        while (temploc > (233 + (self.selection * 48))):
            yvel += 1
            screen.blit(self.bgimage, (0,0))
            temploc -= yvel
            selectloc = (356,temploc)
            screen.blit(self.selectimage, selectloc)
            pygame.display.flip()
            pygame.time.wait(15)
        
            
    def ShowMenu(self, screen):
        #screen.fill((0,0,0))
        pygame.mixer.stop
        #FANCY FADE IN OMG
        for x in range(40):
            screen.fill((0,0,0))
            work = self.bgimage
            work.set_alpha((x * 255) / 40.0, RLEACCEL)
            screen.blit(work, (0,0))
            pygame.display.flip()
            pygame.time.wait(5)
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT) or (event.key == K_DOWN)):
                        self.MoveDown(screen)
                    elif ((event.key == K_LEFT) or (event.key == K_UP)):
                        self.MoveUp(screen)                        
                    elif (event.key == K_ESCAPE):
                        self.selection = 3
                        return self.PickIt(screen)
                    else:
                        self.selsound.play()
                        return self.PickIt(screen)

                elif event.type == JOYAXISMOTION:
                    if ((event.axis == 1) and (event.value < -0.1)):
                        self.MoveUp(screen)
                    elif ((event.axis == 1) and (event.value > 0.1)):
                        self.MoveDown(screen)

                elif event.type == JOYHATMOTION:
                    if ((event.value[1] < -0.1)): #(event.hat == 1) and
                        self.MoveDown(screen)
                    elif ((event.value[1] > 0.1)):
                        self.MoveUp(screen)

                elif event.type == JOYBUTTONDOWN:
                    #pass
                    if (event.button >= 0) and (event.button < 4):
                        self.selsound.play()
                        return self.PickIt(screen)
            
            screen.blit(self.bgimage, (0,0))
            selectloc = (356,233 + (self.selection * 48))
                        
            screen.blit(self.selectimage, selectloc)
            pygame.display.flip()
            pygame.time.wait(25) #
                    
        
