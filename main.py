import tkinter as tk
from playsound import play_quran

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
        for fr in (StartPage,):

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

        #
        self.playing = {"val":False}

        # label (الصفحة الرئيسية)
        label = tk.Label(self, text="الصفحة الرئيسية", font=('Arial 18 bold'))

        # putting the grid in its place by using grid
        label.place(relx=.5, rely=.1, anchor="center")

        # button (تشغيل اليومي)
        quran_btn = tk.Button(self, text="اليومي", font=('Arial 14 bold'), width=10, height=1,
                              command=lambda: play_quran(self.playing))

        quran_btn.place(relx=.8, rely=.3, anchor="se")

        # # button (الذهاب لصفحة القرءان)
        # quran_btn = tk.Button(self, text="القرءان", font=('Arial 14 bold'),
        #                       width=10, height=1)
        # quran_btn.place(relx=.8, rely=.45, anchor="se")

        # # button (الذهاب لصفحة الاغاني)
        # song_btn = tk.Button(self, text="الأغاني", font=('Arial 14 bold'),
        #                      width=10, height=1)
        # song_btn.place(relx=.8, rely=.6, anchor="se")

        # # button (الخروج من البرنامج)
        # exit_btn = tk.Button(self, text="خروج", font=('Arial 14 bold'),
        #                      width=10, height=1)
        # exit_btn.place(relx=.8, rely=.75, anchor="se")


def main():
    app = tkinterApp()

    app.mainloop()


if __name__ == "__main__":
    main()
