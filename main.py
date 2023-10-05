import tkinter as TK
import pygame

window = TK.Tk()
window.title("المعنوي")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = 600
window_height = 600

window.geometry(f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{screen_height//2 - window_height//2}")

def main():
    
    window.mainloop()
     
if __name__ == "__main__":
    main()