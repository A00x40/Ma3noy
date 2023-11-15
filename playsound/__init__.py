import os
from pathlib import Path
from tkinter import Listbox
import random
import pygame
from threading import Thread
from time import sleep

class SoundApp():

    music_thread = None

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()# initialise the pygame
        self.stop_playing = True
 
    def playAll(self, file_list, playlist=None):

        self.stop_playing = False
        for i in range(0, len(file_list)):
            
            if self.stop_playing:
                break

            self.mixer.music.load(file_list[i])
            self.mixer.music.play()

            while self.mixer.music.get_busy():
                continue

            # After song ends move selection tto next
            if playlist != None :
                selection = playlist.curselection()[0]

                print(selection , playlist.itemcount)

                if (selection+1) < playlist.itemcount:
                    playlist.selection_clear(selection)
                    playlist.selection_set(selection+1)
          
    def pause(self):
        self.mixer.music.pause()
        
        

    def stop(self):
        self.mixer.music.stop()
        self.stop_playing = True

sound = SoundApp()

quran_list_dir = os.listdir(f"{Path(__file__).parent.parent}/sound/quran") 
quran_list = []
for filename in quran_list_dir:
    quran_list.append(os.path.join("sound/quran/", filename))

song_list_dir = os.listdir(f"{Path(__file__).parent.parent}/sound/songs") 

# Playlist class
class PlayList(Listbox):
    def __init__(self, parent):
        super().__init__(parent)
        self.itemcount = 0

    def addList(self, items):
        for i in range(len(items)):
            self.insert(i, items[i])
            self.itemcount += 1

    # position: 0 -> from start, (itemcount - 1) -> from end
    def play(self, path, position=-1):

        selected = self.curselection()

        if position != -1:
            if len(selected) != 0:
                self.selection_clear(selected)
            self.selection_set(position)
            selected = [position]
            
        # check if item is selected
        if len(selected) != 0:
            index = selected[0]

            filelist = []
            for i in range(index, self.itemcount):
                filelist.append(f"{path}{self.get(i)}")
            
            if sound.mixer.music.get_busy():
                sound.stop()
            sound.music_thread = Thread(target=sound.playAll, args=(filelist, self,), daemon=True)
            sound.music_thread.start()

    def stop(self):
        sound.stop()

def play_quran(is_playing):
   
    # button click while no sound is playing
    if is_playing["val"] == False:
        is_playing["val"] = True
        
        random.shuffle(quran_list)

        # creatte a thread to run music in background
        # daemon option terminates the thread when the program closes
        sound.music_thread = Thread(target=sound.playAll, args=(quran_list,), daemon=True)
        sound.music_thread.start()
            
    # stop playing sound 
    else:
        is_playing["val"] = False
        sound.stop()
    
