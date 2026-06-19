#!/usr/bin/env python

# This file is basically just a launcher for the game. All the good stuff is in the lib directory.

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

import sys
import os
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, libdir)

import pillows
pillows.Start()
