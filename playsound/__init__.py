from tkinter import Listbox
import pygame
from threading import Thread
from datetime import datetime

def findTime():
    H = int(datetime.now().strftime('%H'))
    M = int(datetime.now().strftime('%M'))
    S = int(datetime.now().strftime('%S'))
    return H, M, S

class SoundApp():

    music_thread = None

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()# initialise the pygame
        self.stop_playing = True
        self.azan_playing = False

    def play(self, file, is_azan=False):

        if is_azan:
            self.azan_playing = True
        
        self.mixer.music.load(file)
        self.mixer.music.play()
        while self.mixer.music.get_busy():
            continue
        self.azan_playing = False
 
    # Daily arr -> [a,b,c] 
    # Single item is a tuple of file names and scheduled times
    def playDaily(self, daily_arr):

        for i in range(0, len(daily_arr)):
            scheduled_time = daily_arr[i][1]
            file_list = daily_arr[i][0]

            H, M, S = findTime()
            
            if(H < scheduled_time[0] or H >= scheduled_time[1]):
                continue

            self.stop_playing = False

            for i in range(0, len(file_list)):
                
                if self.stop_playing:
                    break

                self.mixer.music.load(file_list[i])
                self.mixer.music.play()

                if self.azan_playing:
                    break

                while self.mixer.music.get_busy():
                    if(H < scheduled_time[0] or H >= scheduled_time[1]):
                        break
                    continue
                        
    def playAll(self, file_list, playlist=None):

        self.stop_playing = False

        if not self.azan_playing:
            for i in range(0, len(file_list)):
                
                if self.stop_playing:
                    break

                self.mixer.music.load(file_list[i])
                self.mixer.music.play()

                if self.azan_playing:
                    break

                # A check to not increase cursor
                if self.stop_playing:
                    break

                while self.mixer.music.get_busy():
                    continue

                # After song ends move selection tto next
                if playlist != None :
                    selection = playlist.curselection()[0]

                    if (selection+1) < playlist.itemcount:
                        playlist.selection_clear(selection)
                        playlist.selection_set(selection+1)
          
    def pause(self):
        self.mixer.music.pause()
        
    def stop(self):
        if not self.azan_playing:
            self.mixer.music.stop()
            self.stop_playing = True

sound = SoundApp()


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

        # Check if play has been clicked already
        # Stop action to end the thread
        # Then create a new music_thread 
        if sound.music_thread != None:
            sound.stop()

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
