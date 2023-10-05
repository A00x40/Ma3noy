import tkinter as tk
from tkinter import ttk
import pygame

window_width = 600
window_height = 500

class tkinterApp(tk.Tk):

    # Initialize the application
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title("المعنوي")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{screen_height//2 - window_height//2}")
        self.resizable(False, False)

        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames
        self.frames = {}

        # for each page class create a new frame 
        # with container as its parent
        for fr in (StartPage,):
           
            frame = fr(container, self)
            
            self.frames[fr] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)

    # Display current frame passed
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

# First window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        super().__init__(parent)
         
        # label of frame 
        label = tk.Label(self, text ="الصفحة الرئيسية", font= ('Arial 14 bold'))
        
        # putting the grid in its place by using
        # grid
        label.place(relx=.5, rely=.1, anchor="center")

        # 
        quran_btn = tk.Button(self, text="اليومي", font=('Arial 14 bold'),
        width=10, height=1)
        quran_btn.place(relx=.8, rely=.3, anchor="se")

        # 
        quran_btn = tk.Button(self, text ="القرءان", font= ('Arial 14 bold'),
        width=10, height=1)
        quran_btn.place(relx=.8, rely=.45, anchor="se")

        # 
        song_btn = tk.Button(self, text ="الأغاني", font= ('Arial 14 bold'),
        width=10, height=1)
        song_btn.place(relx=.8, rely=.6, anchor="se")

        # 
        exit_btn = tk.Button(self, text ="خروج", font= ('Arial 14 bold'),
        width=10, height=1)
        exit_btn.place(relx=.8, rely=.75, anchor="se")

def main():
    app = tkinterApp()

    app.mainloop()
    
if __name__ == "__main__":
    main()