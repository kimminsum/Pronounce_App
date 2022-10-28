import csv
import os
import tkinter as tk
from bs4 import BeautifulSoup
import urllib.request

window = tk.Tk()
"""
Read .csv
"""
path = os.path.abspath("word.csv")

word_list = []
try:
    with open(path, "rt", encoding="UTF-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word_list.append(row["Word"])

    print("지금 기입된 단어들:", word_list)

    pronounce_list = []
    for i in range(len(word_list)):
        try:
            print(f"단어 발음 추출 중...{i}/{len(word_list)}")
            url = f"https://dictionary.cambridge.org/ko/%EC%82%AC%EC%A0%84/%EC%98%81%EC%96%B4/{str(word_list[i])}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            request = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(request)
            soup = BeautifulSoup(html, "lxml", from_encoding='UTF-8')
            pronounce = soup.find("span", {"class": "ipa dipa lpr-2 lpl-1"}).get_text()
            pronounce_list.append(pronounce)
        except:
            print("오류가 발생했습니다.")
            pronounce_list.append("N/A")
    """
    Write .csv
    """
    with open(path, "w", newline="", encoding="UTF-8") as f:
        fieldnames = ["Word", "Pronounce"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        print("발음 기입 중")
        for i in range(len(word_list)):
            writer.writerow({"Word" : f"{word_list[i]}", "Pronounce": f"[{pronounce_list[i]}]"})

except Exception as e:
    print(e)