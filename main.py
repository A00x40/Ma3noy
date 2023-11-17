import tkinter as tk
from playsound import sound, PlayList, play_quran, quran_list_dir, song_list_dir
from schedules import Schedules

window_width = 600
window_height = 500


class tkinterApp(tk.Tk):

    # Initialize the application
    def __init__(self):
        super().__init__()

        self.title("المعنوي")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(
            f"{window_width}x{window_height}+{screen_width//2 - window_width//2}+{screen_height//2 - window_height//2}")
        self.resizable(False, False)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames
        self.frames = {}

        # for each page class create a new frame
        # with container as its parent
        for fr in (StartPage, QuranPage, SongPage):

            frame = fr(container, self)

            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # Display current frame passed
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

# First window frame startpage
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)

        # assigning a background image using PhotoImage
        img = tk.PhotoImage(file="./assets/start_bg.png")
        BGlabel = tk.Label(self, image=img)
        BGlabel.image = img
        BGlabel.place(x=0, y=0, width=window_width, height=window_height)

        
        self.playing = {"val": False}

        # label (الصفحة الرئيسية)
        label = tk.Label(self, text="الصفحة الرئيسية", font=('Arial 18 bold'))

        # putting the grid in its place by using grid
        label.place(relx=.5, rely=.1, anchor="center")

        # button (تشغيل اليومي)
        quran_btn = tk.Button(self, text="اليومي", font=('Arial 14 bold'), width=10, height=1,
                              command=lambda: play_quran(self.playing))

        quran_btn.place(relx=.8, rely=.3, anchor="se")

        # button (الذهاب لصفحة القرءان)
        quran_btn = tk.Button(self, text="القرءان", font=('Arial 14 bold'), width=10, height=1,
                              command=lambda: controller.show_frame(QuranPage))
        quran_btn.place(relx=.8, rely=.45, anchor="se")

        # button (الذهاب لصفحة الاغاني)
        song_btn = tk.Button(self, text="الأغاني", font=('Arial 14 bold'), width=10, height=1,
                             command=lambda: controller.show_frame(SongPage))
        song_btn.place(relx=.8, rely=.6, anchor="se")

        # button (الخروج من البرنامج)
        exit_btn = tk.Button(self, text="خروج", font=('Arial 14 bold'), width=10, height=1,
                             command=lambda: controller.destroy())
        exit_btn.place(relx=.8, rely=.75, anchor="se")

# Second window frame quranpage
class QuranPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # assigning a background image using PhotoImage
        img = tk.PhotoImage(file="./assets/quran_bg.png")
        BGlabel = tk.Label(self, image=img)
        BGlabel.image = img
        BGlabel.place(x=0, y=0, width=window_width, height=window_height)

        # label (صفحة القرءان)
        quran_label = tk.Label(self, text="صفحة القرءان", font=('Arial 18 bold'))
        quran_label.place(relx=.5, rely=.1, anchor="center")

        # button (العودة للصفحة الرئيسية)
        quran_btn = tk.Button(self, text="عودة للرئيسية", font=('Arial 14 bold'), width=10, height=1,
                              command=lambda: controller.show_frame(StartPage))
        quran_btn.place(relx=.2, rely=.9, anchor="center")

        # Creating a Listbox
        listbox = PlayList(self)
        listbox.config(bg="green", fg="black", width=45, font=('',12,'bold',))
        listbox.place(relx=.5, rely=.35, anchor="center")
        listbox.addList(quran_list_dir)

        # Creating a Scrollbar and attaching it
        scrollbar = tk.Scrollbar(self, orient="vertical") 
  
        # Adding Scrollbar to the right side 
        scrollbar.pack(side = "right", fill = "y")

        # Attaching Listbox to Scrollbar 
        # Since we need to have a vertical scroll we use yscrollcommand 
        listbox.config(yscrollcommand = scrollbar.set) 
  
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        scrollbar.config(command = listbox.yview)

        # Action buttons 
        play_btn = tk.Button(self, text="لعب", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.play("sound/quran/"))
        play_btn.place(relx=.4, rely=.6, anchor="center")

        stop_btn = tk.Button(self, text="ايقاف", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.stop())
        stop_btn.place(relx=.6, rely=.6, anchor="center")

        fromstart_btn = tk.Button(self, text="من البداية", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.play("sound/quran/", 0))
        fromstart_btn.place(relx=.2, rely=.6, anchor="center")

        fromend_btn = tk.Button(self, text="من النهاية", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.play("sound/quran/", listbox.itemcount - 1))
        fromend_btn.place(relx=.8, rely=.6, anchor="center")

        # button (الخروج من البرنامج)
        exit_btn = tk.Button(self, text="خروج", font=('Arial 14 bold'), width=10, height=1,
                             command=lambda: controller.destroy())
        exit_btn.place(relx=.8, rely=.9, anchor="center")

# Third window frame songpage
class SongPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # assigning a background image using PhotoImage
        img = tk.PhotoImage(file="./assets/start_bg.png")
        BGlabel = tk.Label(self, image=img)
        BGlabel.image = img
        BGlabel.place(x=0, y=0, width=window_width, height=window_height)

        # label (صفحة القرءان)
        song_label = tk.Label(self, text="صفحة الأغاني", font=('Arial 18 bold'))
        song_label.place(relx=.5, rely=.1, anchor="center")

        # button (العودة للصفحة الرئيسية)
        song_btn = tk.Button(self, text="عودة للرئيسية", font=('Arial 14 bold'), width=10, height=1,
                              command=lambda: controller.show_frame(StartPage))
        song_btn.place(relx=.2, rely=.9, anchor="center")

        # Creating a Listbox
        listbox = PlayList(self)
        listbox.config(bg="green", fg="black", width=45, font=('',12,'bold',))
        listbox.place(relx=.5, rely=.35, anchor="center")
        listbox.addList(song_list_dir)

        # Creating a Scrollbar and attaching it
        scrollbar = tk.Scrollbar(self, orient="vertical") 
  
        # Adding Scrollbar to the right side 
        scrollbar.pack(side = "right", fill = "y")

        # Attaching Listbox to Scrollbar 
        # Since we need to have a vertical scroll we use yscrollcommand 
        listbox.config(yscrollcommand = scrollbar.set) 
  
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        scrollbar.config(command = listbox.yview)

        # Action buttons 
        play_btn = tk.Button(self, text="لعب", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.play("sound/songs/"))
        play_btn.place(relx=.4, rely=.6, anchor="center")

        stop_btn = tk.Button(self, text="ايقاف", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.stop())
        stop_btn.place(relx=.6, rely=.6, anchor="center")

        fromstart_btn = tk.Button(self, text="من البداية", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.play("sound/songs/", 0))
        fromstart_btn.place(relx=.2, rely=.6, anchor="center")

        fromend_btn = tk.Button(self, text="من النهاية", font=('Arial 14 bold'), width=7, height=1,
                             command=lambda: listbox.play("sound/songs/", listbox.itemcount - 1))
        fromend_btn.place(relx=.8, rely=.6, anchor="center")

        # button (الخروج من البرنامج)
        exit_btn = tk.Button(self, text="خروج", font=('Arial 14 bold'), width=10, height=1,
                             command=lambda: controller.destroy())
        exit_btn.place(relx=.8, rely=.9, anchor="center")


def main():
    sc = Schedules(30.033333,31.233334,2)
    sc.schedule_prayers()
    
    app = tkinterApp()

    app.mainloop()

    # check to end music thread
    if sound.mixer.music.get_busy():
        sound.stop()
   

if __name__ == "__main__":
    main()
