#import required libraries
import tkinter as tk
from tkinter import ttk

from functools import partial

from PIL import ImageTk, Image

import requests
from io import BytesIO

#create play types and play names
playTypes = ["Offense", "Defense", "Inbounds"]
offenseOptions = ["Shakrinkle", "Buckeyes"]
defenseOptions = ["2-3", "3-2"]
inboundsOptions = ["Stack 1", "Stack 2"]

#create dictionary of images stored in GitHub
imageURLs = {"Shakrinkle":["https://github.com/dmoste/HC_Application_Code/blob/main/shakrinkle1.png?raw=true",
                           "https://github.com/dmoste/HC_Application_Code/blob/main/shakrinkle2.png?raw=true"],
             "Buckeyes":["https://github.com/dmoste/HC_Application_Code/blob/main/buckeyes1.png?raw=true",
                         "https://github.com/dmoste/HC_Application_Code/blob/main/buckeyes2.png?raw=true"],
             "2-3":["https://github.com/dmoste/HC_Application_Code/blob/main/23.png?raw=true"],
             "3-2":["https://github.com/dmoste/HC_Application_Code/blob/main/32.png?raw=true"],
             "Stack 1":["https://github.com/dmoste/HC_Application_Code/blob/main/stack11.png?raw=true",
                        "https://github.com/dmoste/HC_Application_Code/blob/main/stack12.png?raw=true"],
             "Stack 2":["https://github.com/dmoste/HC_Application_Code/blob/main/stack21.png?raw=true",
                        "https://github.com/dmoste/HC_Application_Code/blob/main/stack22.png?raw=true",
                        "https://github.com/dmoste/HC_Application_Code/blob/main/stack23.png?raw=true"]}

imageDict = {"Shakrinkle":[],
             "Buckeyes":[],
             "2-3":[],
             "3-2":[],
             "Stack 1":[],
             "Stack 2":[]}

def fillOptionsFrame():
    playTypeLabel = tk.Label(master = optionsFrame,
                             text = "Pick a play type...",
                             bg = "White").grid(row = 0, column = 0)
    
    global groupOptionsVar
    groupOptionsVar = tk.StringVar()
    groupOptionsVar.set(playTypes[0])
    
    groupOptions = ttk.Combobox(master = optionsFrame,
                                textvariable = groupOptionsVar, 
                                values = playTypes).grid(row = 1, column = 0)
    chooseGroupButton = tk.Button(master = optionsFrame,
                                  text = "Choose",
                                  width = 10,
                                  height = 1,
                                  command = getGroup).grid(row = 2, column = 0)
    
    optionsFrame.grid(row = 0, column = 1)

def fillDiagramFrame():
    diagramCanvas = tk.Canvas(master = diagramFrame,
                              height = 400,
                              width = 400,
                              bg = "White").grid(row = 0, column = 0, columnspan = 3)
    
    diagramFrame.grid(row = 0, column = 0)
    
def getImages():
    for key in imageURLs.keys():
        for link in imageURLs[key]:
            response = requests.get(link)
            imageDict[key].append(response)

def clearOptionsFrame():
    for widget in optionsFrame.winfo_children():
        widget.destroy()

def getGroup():
    group = groupOptionsVar.get()
    
    clearOptionsFrame()
    fillOptionsFrame()
    
    if group == "Offense":
        for i, play in enumerate(offenseOptions):
            tk.Button(master = optionsFrame,
                      text = play,
                      command = partial(showPlay, play, 0)).grid(row = i+3, column = 0)
    elif group == "Defense":
        for i, play in enumerate(defenseOptions):
            tk.Button(master = optionsFrame,
                      text = play,
                      command = partial(showPlay, play, 0)).grid(row = i+3, column = 0)
    else:
        for i, play in enumerate(inboundsOptions):
            tk.Button(master = optionsFrame,
                      text = play,
                      command = partial(showPlay, play, 0)).grid(row = i+3, column = 0)

def showPlay(play, n):
    numDiagrams = len(imageDict[play])
    
    if n >= numDiagrams:
        n = numDiagrams-1
    elif n < 0:
        n = 0
    
    load = Image.open(BytesIO(imageDict[play][n].content))
    render = ImageTk.PhotoImage(load.resize((400, 355), Image.ANTIALIAS))
    playImage = tk.Label(master = diagramFrame,
                         image = render)
    playImage.image = render
    playImage.grid(row = 0, column = 0, columnspan = 3)
    
    backButton = tk.Button(master = diagramFrame,
                           text = "Back",
                           command = partial(showPlay, play, n-1)).grid(row = 1, column = 0)
    
    locationLabel = tk.Label(master = diagramFrame,
                             text = "{}/{}".format(n+1, numDiagrams),
                             bg = "White").grid(row = 1, column = 1)
    
    forwardButton = tk.Button(master = diagramFrame,
                              text = "Next",
                              command = partial(showPlay, play, n+1)).grid(row = 1, column = 2)

window = tk.Tk()
diagramFrame = tk.Frame(master = window,
                        height = 400,
                        width = 400,
                        bg = "White")
optionsFrame = tk.Frame(master = window,
                        height = 400,
                        width = 100,
                        bg = "White")

getImages()
fillOptionsFrame()
fillDiagramFrame()

window.mainloop()
