from bs4 import BeautifulSoup
import urllib.request

import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk
import threading

import csv
import os

class Pronounce_App:
    def __init__(self):
        self.csv_path = os.path.abspath("word.csv")
        self.word_list = []
        self.pronounce_list = []
        self.initial_root()
    """
    Initial Setting -> Root
    """
    def initial_root(self):
        self.root = tk.Tk()
        self.root.title("영어 발음 추출기")
        self.root.geometry("200x80+800+300")
        self.root.resizable(False, False)
        ### Start Button Entity
        start_button_frame = tk.Frame(self.root)
        start_button_frame.pack()

        start_button = tk.Button(start_button_frame, text="발음 추출하기", command=lambda:self.start_when_button_is_down(start_button))
        start_button.place(anchor=tk.CENTER) # Setting Button Place -> Center
        start_button.pack()
        self.root.mainloop()
    """
    Start Button
    """
    def start_when_button_is_down(self, widget):
        widget.pack_forget()
        ### <----o-->
        progressbar=tkinter.ttk.Progressbar(self.root, maximum=100, mode="indeterminate")
        progressbar.pack()
        progressbar.start(50)
        progress_box_frame = tk.Frame(self.root)
        progress_box_frame.pack()
        self.progress_box = tk.Label(progress_box_frame, fg="white")
        self.progress_box.pack()

        t = threading.Thread(target=self.crawling_pronounce)
        t.start()
        self.root.mainloop()
    """
    Crawling Pronounce from -> https://dictionary.cambridge.org/ko/
    """
    def crawling_pronounce(self):
        try:
            ### Insert English Word in word_list
            with open(self.csv_path, "rt", encoding="UTF-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.word_list.append(row["Word"])
            for i in range(len(self.word_list)):
                try:
                    # print(f"단어 발음 추출 중...{i}/{len(self.word_list)}")
                    self.progress_box.config(text=f"단어 발음 추출 중...{i+1}/{len(self.word_list)}")
                    url = f"https://dictionary.cambridge.org/ko/%EC%82%AC%EC%A0%84/%EC%98%81%EC%96%B4/{self.word_list[i]}"
                    headers = {'User-Agent': 'Mozilla/5.0'} # Hacking I'm not bot
                    request = urllib.request.Request(url, headers=headers)
                    html = urllib.request.urlopen(request)
                    soup = BeautifulSoup(html, "lxml", from_encoding='UTF-8')
                    ### Find Elements
                    pronounce = soup.find("span", {"class": "ipa dipa lpr-2 lpl-1"}).get_text()
                    ### Insert Data
                    self.pronounce_list.append(pronounce)
                except:
                    ### If something is wrong, Skip maybe 503 Error
                    # print("오류가 발생했습니다.")
                    self.progress_box.config(text="오류가 발생했습니다.")
                    self.pronounce_list.append("N/A")
            """
            Write .csv
            """
            with open(self.csv_path, "w", newline="", encoding="UTF-8") as f:
                fieldnames = ["Word", "Pronounce"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                # print("발음 기입 중")
                self.progress_box.config(text="발음 기입 중...")
                for i in range(len(self.word_list)):
                    writer.writerow({"Word" : f"{self.word_list[i]}", "Pronounce": f"[{self.pronounce_list[i]}]"})
            msgbox.showinfo("알림", "모든 발음을 작성했습니다.")
            self.root.destroy()
        except:
            msgbox.showerror("오류","파일이 열리지 않습니다.")
            self.root.destroy()
    """
    Update Current Progress
    """
    def progress_update(self, txt):
        self.progress_box.config(text=f"{txt}")

if __name__=="__main__":
    Pronounce_App()