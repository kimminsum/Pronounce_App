from gc import callbacks
import tkinter as tk
from typing import Literal

class Pronounce_App:
    def __init__(self):
        self.num = 0
        self.root = tk.Tk()
        self.root.title("영어 발음 추출기")
        self.root.geometry("200x80+800+300")
        self.root.resizable(False, False)
        ### Start Button Entity
        start_button_frame = tk.Frame(self.root)
        start_button_frame.pack()

        start_button = tk.Button(start_button_frame, text="Start Button", command=lambda:self.start_when_button_is_down(start_button))
        start_button.place(anchor=tk.CENTER) # Setting Button Place -> Center
        start_button.pack()
        self.root.mainloop()
    """
    Start Button
    """
    def start_when_button_is_down(self, widget):
        widget.pack_forget()
        self.start_root()
    """
    Init
    """
    def start_root(self):
        progress_box_frame = tk.Frame(self.root)
        progress_box_frame.pack()
        self.progress_box = tk.Label(progress_box_frame, fg="white")
        self.progress_box.pack()
        self.progress_update()
    """
    Update Current Progress
    """
    def progress_update(self):
        self.num += 1
        self.progress_box.config(text=f"{self.num}")
        self.progress_box.after(200, self.progress_update)

if __name__=="__main__":
    Pronounce_App()