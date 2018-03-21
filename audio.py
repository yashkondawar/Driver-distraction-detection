# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 20:01:37 2018

@author: Dell
"""

from pygame import mixer

def audioplay(pl):
    if pl == True:
        mixer.init()
        mixer.music.load('G:\Songs Pen Drive\Songs\Happy new year\manva.mp3')
        mixer.music.play()

audioplay(True)        
