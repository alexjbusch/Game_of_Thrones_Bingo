from tkinter import *
from PIL import ImageGrab
from pathlib import Path
import os
import random

from ctypes import windll
user32 = windll.user32
user32.SetProcessDPIAware()

root = Tk()
root.attributes("-fullscreen", True)


pool = []
possible_deaths = []
possible_survival = []
theories = []
ships = []

def RetrieveData():
    pd = False
    ps = False
    th = False
    sh = False
    
    f = open("got_bingo.txt","r")
    for line in f:
        line = line.strip()
        if str(line) == "possible deaths":
            pd = True
            continue
        elif line == "possible survival":
            ps = True
            continue
        elif line == "theories":
            th = True
            continue
        elif line == "ships":
            sh = True
            continue
        elif line == "*":
            pd = False           
            ps = False
            th = False
            sh = False

        if pd:
            possible_deaths.append(line)
        elif ps:
            possible_survival.append(line)
        elif th:
            theories.append(line)
        elif sh:
            ships.append(line)


    index = 0
    for i in possible_deaths:
        i += " dies"
        possible_deaths[index] = i
        index += 1
    index = 0
    for i in possible_survival:
        i += " survives"
        possible_survival[index] = i
        index += 1
    global pool
    pool = possible_deaths + possible_survival + theories + ships


def CreateGrid():
    used = []
    for x in range(5):
        for y in range(5):
            if x == 2 and y == 2:
                txt = "Main Chracter Death \n FREE SPACE"
            else:
                invalid = True
                while invalid:
                    index = random.randrange(0,len(pool))
                    txt = pool[index]
                    if txt in used:
                        continue
                    if txt in possible_survival:
                        if txt[:-9] + " dies" in used:
                            #print(txt)
                            continue
                    if txt in possible_deaths:
                        if txt[:-5] + " survives" in used:
                            #print(txt)
                            continue
                    invalid = False
                
                used.append(txt)

            btn = Button(root,wraplength=150,text=txt)
            btn.grid(column=y, row=x, sticky=N+S+E+W)
            btn.config( height = 8, width = 23,font='Helvetica 12 bold' )


def TakeScreenshot():
    im = ImageGrab.grab(bbox=(0,0,1430,1050))
    number = 0
    saved = False
    if not os.path.isdir("Bingo_Cards"):
        os.mkdir("Bingo_Cards")
    while not saved:
        my_file = Path(os.path.dirname(os.path.realpath(__file__))+"\\Bingo_Cards\\Bingo_Card"+str(number)+".png")
        if my_file.is_file():
            number += 1
            continue
        else:            
            im.save("Bingo_Cards\\Bingo_Card"+str(number)+".png")
            saved = True

def CreateScreenshot():
    CreateGrid()
    TakeScreenshot()

RetrieveData()
CreateGrid()

#BUTTONS
randomize_button = Button(root, text="Randomize", command=CreateGrid)
randomize_button.place(x = 1500, height = 100,width=250)

screenshot_button = Button(root, text="Get PNG of this card", command=TakeScreenshot)
screenshot_button.place(x = 1500, y =100,height = 100,width=250)

create_screenshot_button = Button(root, text="Create new card and get PNG of it", command=CreateScreenshot)
create_screenshot_button.place(x = 1500, y =200,height = 100,width=250)
#END BUTTONS

root.mainloop()

#TakeScreenshot()

