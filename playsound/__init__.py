import os
from pathlib import Path
import random
import pygame

class SoundApp():

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()# initialise the pygame
 
    def playAll(self, file_list):

        self.mixer.music.load(file_list[0])
        for i in range(1, len(file_list)):
            self.mixer.music.queue(file_list[i])
        self.mixer.music.play()

    def pause(self):
        self.mixer.music.pause()

    def stop(self):
        self.mixer.music.stop()

sound = SoundApp()


quran_list_dir = os.listdir(f"{Path(__file__).parent.parent}/sound/quran") 
quran_list = []
for filename in quran_list_dir:
    quran_list.append(os.path.join("sound/quran/", filename))

def play_quran(is_playing):
   
    # button click while no sound is playing
    if is_playing["val"] == False:
        is_playing["val"] = True
        
        random.shuffle(quran_list)
        sound.playAll(quran_list)
            
    # stop playing sound 
    else:
        is_playing["val"] = False
        sound.stop()
    
