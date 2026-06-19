# Milk.py goes great with cookies!
# Just kidding, this is the fun little particle engine for the firey particles that
#     shoot out the back of the missile.

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

import pygame
import random
from pygame.locals import *

#from locals import *

class Particle (pygame.sprite.Sprite):
    def __init__(self, position, vect, colour, acceleration, size, life, opacity, underwater = True):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(position[0], position[1], size, size)
        self.vect = vect
        self.colour = colour
        self.acceleration = acceleration
        self.initial_life = life
        self.life = life
        self.opacity = opacity
        self.underwater = underwater

        self.image = pygame.Surface([int(size), int(size)])#, SRCALPHA, 32)
        self.image.fill((255,0,255))
        self.image.set_colorkey((255,0,255))

        pygame.draw.ellipse(self.image, self.colour, self.image.get_rect())

        #if Variables.alpha:
        self.image.set_alpha(self.life * 255 * self.opacity / self.initial_life)

    def update(self):
        self.rect.left += self.vect[0]
        self.rect.top += self.vect[1]
        self.vect[0] += self.acceleration[0]
        self.vect[1] += self.acceleration[1]
        if self.life > 0:
            self.life -= 1

        if not self.underwater and self.vect[1] > 0.0:
            self.life = 0

        #if Variables.alpha:
        self.image.set_alpha(self.life * 255 * self.opacity / self.initial_life)

class Particles (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.particles = []
        self.particle_sprites = pygame.sprite.Group()
        #if Variables.alpha:
        self.image = pygame.Surface((640, 480), SRCALPHA, 32)
        #else:
        #self.image = pygame.Surface((640, 480))
        #self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()

    def update(self):
        self.image.fill((255,0,255,0))
        
        self.particle_sprites.draw(self.image)

        for p in self.particles:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)
                self.particle_sprites.remove(p)

    def add_steam_particle(self, position):
        particle = Particle(position, [0, -random.random() * 0.4], [240, 240, 240], [-0.0, -0.15], random.random() * 14.0 + 2.0, random.random() * 30, 0.4)
        self.particles.append(particle)
        self.particle_sprites.add(particle)
        
    def add_fire_steam_particle(self, position):
        particle = Particle(position, [0, -random.random() * 0.5], [255, 110, 70], [-0.0, -0.15], random.random() * 10.0 + 1.0, random.random() * 30, 0.8, False)
        self.particles.append(particle)
        self.particle_sprites.add(particle)

        
