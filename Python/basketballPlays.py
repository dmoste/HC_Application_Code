#import tkinter GUI library - ttk required for combobox
import tkinter as tk
from tkinter import ttk

#imprt partial to send arguments from tkinter commands
from functools import partial

#import pillow to handle the images
from PIL import ImageTk, Image

#import requests and BytesIO to get images from internet links
import requests
from io import BytesIO

#create play types and play names
playTypes = ["Offense", "Defense", "Inbounds"]
offenseOptions = ["Shakrinkle", "Buckeyes"]
defenseOptions = ["2-3", "3-2"]
inboundsOptions = ["Stack 1", "Stack 2"]

#setup the common portion of the links string
strStart = "https://github.com/dmoste/HC_Application_Code/blob/main/Python/"
strEnd = ".png?raw=true"

#create dictionary of images stored in GitHub
imageURLs = {"Shakrinkle":[strStart + "shakrinkle1" + strEnd, strStart + "shakrinkle2" + strEnd],
             "Buckeyes":[strStart + "buckeyes1" + strEnd, strStart + "buckeyes2" + strEnd],
             "2-3":[strStart + "23" + strEnd],
             "3-2":[strStart + "32" + strEnd],
             "Stack 1":[strStart + "stack11" + strEnd, strStart + "stack12" + strEnd],
             "Stack 2":[strStart + "stack21" + strEnd, strStart + "stack22" + strEnd, strStart + "stack23" + strEnd]}

imageDict = {"Shakrinkle":[],
             "Buckeyes":[],
             "2-3":[],
             "3-2":[],
             "Stack 1":[],
             "Stack 2":[]}

def fillOptionsFrame():
    #add instructions to use as a label
    playTypeLabel = tk.Label(master = optionsFrame,
                             text = "Pick a play type...",
                             bg = "White").grid(row = 0, column = 0)
    
    #create StringVar to hold variable options for the combobox - needs to be seen by other functions
    global groupOptionsVar
    groupOptionsVar = tk.StringVar()
    groupOptionsVar.set(playTypes[0])
    
    #create combobox to display play types
    groupOptions = ttk.Combobox(master = optionsFrame,
                                textvariable = groupOptionsVar, 
                                values = playTypes).grid(row = 1, column = 0)
    
    #create button to select play type
    chooseGroupButton = tk.Button(master = optionsFrame,
                                  text = "Choose",
                                  width = 10,
                                  height = 1,
                                  command = getGroup).grid(row = 2, column = 0)
    
    #populate the frame
    optionsFrame.grid(row = 0, column = 1)

def fillDiagramFrame():
    #create canvas object to hold the images
    diagramCanvas = tk.Canvas(master = diagramFrame,
                              height = 400,
                              width = 400,
                              bg = "White").grid(row = 0, column = 0, columnspan = 3)
    
    #populate the frame
    diagramFrame.grid(row = 0, column = 0)
    
def getImages():
    #go to each image link, download the image, and add it to a dictionary
    for key in imageURLs.keys():
        for link in imageURLs[key]:
            response = requests.get(link)
            imageDict[key].append(response)

def clearOptionsFrame():
    #clear every widget in the options frame
    for widget in optionsFrame.winfo_children():
        widget.destroy()

def getGroup():
    #get the value from the combobox
    group = groupOptionsVar.get()
    
    #clear, then refill the options frame - destroys old buttons when new options are selected
    clearOptionsFrame()
    fillOptionsFrame()
    
    #add directions for the user
    listPlaysLabel = tk.Label(master = optionsFrame,
                              text = "Pick a play from the options below",
                              bg = "White").grid(row = 3, column = 0)
    
    #create buttons to select a play based on the play type chosen
    if group == "Offense":
        for i, play in enumerate(offenseOptions):
            tk.Button(master = optionsFrame,
                      text = play,
                      command = partial(showPlay, play, 0)).grid(row = i+4, column = 0)
    elif group == "Defense":
        for i, play in enumerate(defenseOptions):
            tk.Button(master = optionsFrame,
                      text = play,
                      command = partial(showPlay, play, 0)).grid(row = i+4, column = 0)
    else:
        for i, play in enumerate(inboundsOptions):
            tk.Button(master = optionsFrame,
                      text = play,
                      command = partial(showPlay, play, 0)).grid(row = i+4, column = 0)

def showPlay(play, n):
    #get the number of images for the chosen play
    numDiagrams = len(imageDict[play])
    
    #correct n in case it becomes more than the maximum number of images or less than 0
    if n >= numDiagrams:
        n = numDiagrams-1
    elif n < 0:
        n = 0
    
    #load the first image of the chosen play, resize it, then toss it onto the canvas
    load = Image.open(BytesIO(imageDict[play][n].content))
    render = ImageTk.PhotoImage(load.resize((400, 355), Image.ANTIALIAS))
    playImage = tk.Label(master = diagramFrame,
                         image = render)
    playImage.image = render
    playImage.grid(row = 0, column = 0, columnspan = 3)
    
    #create a button to see the previous image
    backButton = tk.Button(master = diagramFrame,
                           text = "Previous",
                           command = partial(showPlay, play, n-1)).grid(row = 1, column = 0)
    
    #create a button to display how many images there are and which image the user is viewing
    locationLabel = tk.Label(master = diagramFrame,
                             text = "{}/{}".format(n+1, numDiagrams),
                             bg = "White").grid(row = 1, column = 1)
    
    #create a button to see the next image
    forwardButton = tk.Button(master = diagramFrame,
                              text = "Next",
                              command = partial(showPlay, play, n+1)).grid(row = 1, column = 2)

#create a window
window = tk.Tk()

#create the two required frames for this application
diagramFrame = tk.Frame(master = window,
                        height = 400,
                        width = 400,
                        bg = "White")
optionsFrame = tk.Frame(master = window,
                        height = 400,
                        width = 200,
                        bg = "White")

#get all the images of the plays at the start so the user doesn't have to wait after each play selection
getImages()

#fill both frames
fillOptionsFrame()
fillDiagramFrame()

#listen for events until the application is closed
window.mainloop()
