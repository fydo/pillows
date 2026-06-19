# This is the actual game! It's fun ;)

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

import os, sys, math, random
import pygame
from pygame.locals import *
from math import *
from milk import Particles

LogicalFPS = 64.0
TicksPerFrame = (1000.0 / LogicalFPS)
MaxFrameSkip = 2

class Missile:
    def __init__(self):
        self.rect = (random.randint(150, 550),-100) #defaults
        self.image = pygame.image.load(os.path.join('data', 'rocket.png')).convert_alpha()
        self.curFrame = 0
        self.timer = 0.00
        self.speed = 15
        self.angle = 0
        
class Launcher:
    def __init__(self):
        self.rect = (0, 330)
        self.image = pygame.image.load(os.path.join('data', 'catapult.png')).convert_alpha()
        self.launching = False
        self.empty = False
        self.rewind = False
        self.timer = 0.00
        self.curFrame = 0
        self.speed = 60
    
class Pillow:
    def __init__(self, velocity):
        self.vx = velocity[0]
        self.vy = -velocity[1]
        self.rect = (30, 300) #default launching location
        self.landed = False
        self.curFrame = 2
        self.timer = 0.00

class Game:
    def __init__(self, noSound):
        self.missile = Missile()
        self.launcher = Launcher()
        self.level = 1
        self.pillows = []
        self.imglevel = pygame.image.load(os.path.join('data', 'stage.png')).convert()
        hud = pygame.image.load(os.path.join('data', 'hud.png')).convert_alpha()
        self.imglevel.blit(hud, (0,0))
        self.powerbar = pygame.image.load(os.path.join('data', 'power.png')).convert()
        self.shadow = pygame.image.load(os.path.join('data', 'shadow.png')).convert_alpha()
        self.imgpillow = pygame.image.load(os.path.join('data', 'pillow.png')).convert_alpha()
        self.winlevelimage = pygame.image.load(os.path.join('data', 'winlevel.png')).convert_alpha()
        self.countdownimage = pygame.image.load(os.path.join('data', 'countdown.png')).convert_alpha()
        self.pillowland = pygame.mixer.Sound(os.path.join('data', 'pillowland.ogg'))
        self.catasound = pygame.mixer.Sound(os.path.join('data', 'cata-shot.ogg'))
        self.noshotsound = pygame.mixer.Sound(os.path.join('data', 'nopillow.ogg'))
        self.countone = pygame.mixer.Sound(os.path.join('data', 'one.ogg'))
        self.counttwo = pygame.mixer.Sound(os.path.join('data', 'two.ogg'))
        self.countthree = pygame.mixer.Sound(os.path.join('data', 'three.ogg'))
        self.countgo = pygame.mixer.Sound(os.path.join('data', 'go.ogg'))
        pygame.mixer.music.load(os.path.join('data', 'jdruid_the_less_i_know.ogg'))
        pygame.mixer.music.set_volume(0.6)
        self.particles = Particles()
        self.particle_sprite = pygame.sprite.Group()
        self.particle_sprite.add(self.particles)
        self.thetime = 0.0000
        self.timerdiff = 0
        self.noSound = noSound
        self.thefont = pygame.font.Font(os.path.join('data', 'Vera.ttf'), 12)
        self.AllowAim = True
        self.AllowPower = False
        self.CurrentShotAngle = 0.00
        self.CurrentShotPower = 0
        self.PowerMoveUp = True
        self.PowerMoveSpeed = 80
        self.AngleMoveUp = True
        self.AngleMoveSpeed = 40
        self.AngleRects = ((32, 120), (125, 120))
        self.PillowCount = 0
        self.TotalPillowCount = 0
        self.PlayerSavedTheEarth = False
        self.CountingDown = True
        self.CountCount = 0.00
        self.CountFrame = 4
        self.saveSpeed = 0.0
        self.spedUp = False
    
    def Increasespeed(self):
        if self.spedUp == False:
            self.saveSpeed = self.missile.speed
            self.missile.speed = self.missile.speed * 5
            self.spedUp = True
    
    def Normalspeed(self):
        if self.spedUp == True:
            self.spedUp = False
            self.missile.speed = self.saveSpeed
        
    def SetupForNextLevel(self):
        self.level += 1
        self.missile.speed += 6
        self.missile.rect = (random.randint(150, 550),-100)
        self.AllowAim = True
        self.AllowPower = False
        self.CurrentShotAngle = 0.00
        self.CurrentShotPower = 0
        self.PowerMoveUp = True
        self.PowerMoveSpeed = 80
        self.AngleMoveUp = True
        self.AngleMoveSpeed = 40
        self.AngleRects = ((32, 120), (100, 120))
        self.PillowCount = 0
        self.PlayerSavedTheEarth = False
        self.pillows = []
        self.launcher.launching = False
        self.launcher.empty = False
        self.launcher.rewind = False
        self.launcher.timer = 0.00
        self.launcher.curFrame = 0
        self.CountCount = 0.00
        self.CountFrame = 4
    
    def DoInputStuff(self):
        #input!
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    #self.music.fadeout(500)
                    return False
                if (event.key == K_DOWN):
                    self.Increasespeed();
                else:
                    if self.CountingDown == False:
                        self.ButtonDown()
                    
            elif event.type == KEYUP:
                if (event.key == K_DOWN):
                    self.Normalspeed();
                else:
                    self.ButtonUp()
                    
            elif (event.type == MOUSEBUTTONDOWN) or ((event.type == JOYBUTTONDOWN) and (event.button >= 0) and (event.button < 4)):
                self.ButtonDown()
            elif (event.type == MOUSEBUTTONUP) or ((event.type == JOYBUTTONUP) and (event.button >= 0) and (event.button < 4)):
                self.ButtonUp()
            elif (event.type == JOYHATMOTION):
                if ((event.value[1] < -0.1)): #(event.hat == 1) and
                    self.Increasespeed();
                elif ((event.value[1] == 0)):
                    self.Normalspeed();
            elif (event.type == JOYAXISMOTION):
                if ((event.axis == 1) and (event.value > 0.1)):
                    self.Increasespeed();
                elif ((event.axis == 1) and (event.value < 0.1)):
                    self.Normalspeed();
                    
        return True
        
    def ComputeAngleRects(self):
        x = 32
        y = 120
        hyp = 95
        if (self.CurrentShotAngle >= 75):
            self.AngleMoveUp = False
            #self.AngleRects = (self.AngleRects[0], (50, 30))		
        elif (self.CurrentShotAngle <= 0):
            self.AngleMoveUp = True
            #self.AngleRects = (self.AngleRects[0], (100, 130))
        
        self.AngleRects = (self.AngleRects[0], (x + (hyp * cos(radians(self.CurrentShotAngle))), y - (hyp * sin(radians(self.CurrentShotAngle)))))
        
    def ComputeMovement(self, delta):
        self.missile.timer += delta
        if self.missile.timer > 0.02:
            self.missile.curFrame += 1
            self.missile.timer = 0
            self.particles.add_fire_steam_particle((self.missile.rect[0] + 30, self.missile.rect[1]))
                
            if self.missile.curFrame > 31:
                self.missile.curFrame = 0
                
        self.missile.rect = (self.missile.rect[0], self.missile.rect[1] + (delta * self.missile.speed))
        
        if self.AllowAim:
            if self.AngleMoveUp:
                self.CurrentShotAngle += (delta * self.AngleMoveSpeed)
            else:
                self.CurrentShotAngle -= (delta * self.AngleMoveSpeed)
            self.ComputeAngleRects()
            
        if self.AllowPower:
            if self.CurrentShotPower >= 100:
                self.PowerMoveUp = False
            elif self.CurrentShotPower <= 0:
                self.PowerMoveUp = True
                
            if self.PowerMoveUp:
                self.CurrentShotPower += (delta * self.PowerMoveSpeed)
            else:
                self.CurrentShotPower -= (delta * self.PowerMoveSpeed)
                
        if self.launcher.launching:
            self.launcher.timer += delta
            if self.launcher.timer > 0.03:
                self.launcher.curFrame += 1
                self.launcher.timer = 0.00
                if self.launcher.curFrame == 4:
                    self.LaunchPillow()
        elif self.launcher.rewind:
            self.launcher.timer += delta
            if self.launcher.timer > 0.03:
                self.launcher.curFrame -= 1
                self.launcher.timer = 0.00
                if self.launcher.curFrame == 0:
                    self.launcher.rewind = False
                    self.AllowAim = True
                    self.CurrentShotPower = 0
                    self.launcher.empty = False
                    
        #for each pillow in the collection
        for p in self.pillows:
            if p.landed == False:
                #if not landed, iterate the curframe
                p.timer += delta
                if p.timer > 0.025:
                    p.timer = 0.00
                    p.curFrame += 1
                    if p.curFrame == 10:
                        p.curFrame = 0
                #calc pillow placement
                p.vy = p.vy + (300 * delta)
                if (p.rect[0] + 64) > 640:
                    p.vx = -p.vx
                p.rect = ((p.rect[0] + (delta * p.vx)), (p.rect[1] + (delta * p.vy)))
                #check y to see if landed needs to be set
                if p.rect[1] > 395:
                    if not self.noSound:
                        self.pillowland.play()
                    p.landed = True
                    p.curFrame = 0
                    self.launcher.rewind = True
            else:
                if ((self.missile.rect[1] +128) > (p.rect[1] + 45)):
                    if (self.missile.rect[0] > (p.rect[0] - 19)) and (self.missile.rect[0] < (p.rect[0] + 19)):
                        p.curFrame = 10
                        p.rect = (self.missile.rect[0], p.rect[1])
                        self.PlayerSavedTheEarth = True
        
    def LaunchPillow(self):
        self.launcher.launching = False
        self.launcher.empty = True
        #add a pillow to the pillow collection with proper x and y forces
        self.pillows.append(Pillow((((self.CurrentShotPower * 4) * cos(radians(self.CurrentShotAngle))),((self.CurrentShotPower * 4) * sin(radians(self.CurrentShotAngle))))))
                        
    def ButtonDown(self):
        if self.AllowAim:
            self.AllowAim = False
            self.AllowPower = True
            self.PowerMoveUp = True
        else:
            if not self.noSound:
                self.noshotsound.play()
            
    def ButtonUp(self):
        if self.AllowPower:
            #self.AllowAim = True
            self.AllowPower = False
            self.PillowCount += 1
            self.TotalPillowCount += 1
            self.launcher.timer = 0.00
            self.launcher.launching = True
            if not self.noSound:
                self.catasound.play()
    
    def CheckIntersections(self):
        if ((self.missile.rect[1] + 128 ) > 456):
            return False
        else:
            return True
    
    def drawStatus(self, screen, statustext):
        statusBar = pygame.Surface((640, 16)).convert()
        statusBar.fill((20,20,20))
        screen.blit(statusBar, (0, 0))
    
        text = self.thefont.render(statustext, 1, (255,255,255))
        textpos = text.get_rect(centerx = screen.get_width()/2, centery = ((text.get_height()/2)))
        screen.blit(text, textpos)
    
    def Go(self, screen):
        #init stuff
            
        #init timer things
        LastTicks = 0
        ElapsedTicks = 0
    
        #play music
        if (not self.noSound):
            pygame.mixer.music.play(-1)
                
        while 1:
            self.thetime = pygame.time.get_ticks()
            ElapsedTicks += self.thetime - LastTicks
            LastTicks = self.thetime
            
            if (ElapsedTicks > (TicksPerFrame * 4)):
                ElapsedTicks = 0

            frames = 0
            
            #self.particles.add_steam_particle((self.missile.rect[0] + 28, self.missile.rect[1]))
            
            if (ElapsedTicks > TicksPerFrame):
                while ((ElapsedTicks > TicksPerFrame) and (frames < MaxFrameSkip)):
                    ElapsedTicks -= TicksPerFrame
                    timestep = 1.0 / LogicalFPS
                    
                    
                    # everyone loves input
                    if (self.DoInputStuff() == False):
                        pygame.mixer.music.stop()
                        return (self.level, self.TotalPillowCount)
                            
                    if self.CountingDown == False:
                        # compute movements
                        if (self.ComputeMovement(timestep) == False):
                            pygame.mixer.music.stop()
                            return (self.level, self.TotalPillowCount)
                
                        # check for intersects
                        if (self.CheckIntersections() == False):
                            pygame.mixer.music.stop()
                            return (self.level, self.TotalPillowCount)
                    else:
                        self.CountCount += timestep
                    frames += 1
                    
            # draw everything!
            screen.blit(self.imglevel, (0, 0))
            pygame.draw.line(screen, (40,180,40), self.AngleRects[0], self.AngleRects[1], 2)
            screen.blit(self.powerbar, (8, 120 - self.CurrentShotPower), (0, 100 - self.CurrentShotPower, 16, self.CurrentShotPower))
            
            for p in self.pillows:
                screen.blit(self.shadow, (p.rect[0], 442))
                screen.blit(self.imgpillow, (p.rect), ((p.curFrame * 64), 0, 64, 64))
            
            if self.launcher.empty:
                screen.blit(self.launcher.image, (self.launcher.rect), ((self.launcher.curFrame * 200), 0, 200, 150))
            else:
                screen.blit(self.launcher.image, (self.launcher.rect), ((self.launcher.curFrame * 200), 150, 200, 150))
            
            self.particles.update()
            
            if self.CountingDown:
                if (self.CountCount > 0.0) and (self.CountFrame == 4):
                    if not self.noSound:
                        self.countthree.play()
                    self.CountFrame = 3
                elif (self.CountCount > 1.0) and (self.CountFrame == 3):
                    if not self.noSound:
                        self.counttwo.play()
                    self.CountFrame = 2
                elif (self.CountCount > 2.0) and (self.CountFrame == 2):
                    if not self.noSound:
                        self.countone.play()
                    self.CountFrame = 1
                elif (self.CountCount > 3.0) and (self.CountFrame == 1):
                    if not self.noSound:
                        self.countgo.play()
                    self.CountFrame = 0
                elif (self.CountCount > 4.0) and (self.CountFrame == 0):
                    self.CountingDown = False
                    # Purge input queue
                    pygame.event.get()
                
                thewidth = 64
                if self.CountFrame == 0:
                    thewidth = 128
                
                screen.blit(self.countdownimage, (288, 208), ((3-self.CountFrame)*64,0,thewidth,64))
            else:
                screen.blit(self.missile.image, (self.missile.rect), ((self.missile.curFrame * 64), 0, 64, 128))
                self.particle_sprite.draw(screen)
            
            if self.PlayerSavedTheEarth:
                self.drawStatus(screen, "NEXT LEVEL: %d!" % (self.level + 1) )
                screen.blit(self.winlevelimage, (120,90))
                pygame.display.flip()
                pygame.time.wait(2500)
                self.SetupForNextLevel()
                self.CountingDown = True
            else:
                self.drawStatus(screen, "Level: %d    Pillows: %d    Total Pillows: %d" % (self.level, self.PillowCount, self.TotalPillowCount))
                        
            #if self.timerdiff == 0:
                #timer = pygame.time.get_ticks()
            #self.timerdiff = ((pygame.time.get_ticks() - self.thetime) / 1000.000)#convert to seconds
            pygame.display.flip()
            # delay time
            pygame.time.wait(10)
