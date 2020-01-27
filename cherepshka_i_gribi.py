from tkinter import*

window = Tk()
window.title("Черепашка и грибы")
window.geometry("800x600")
mainmenu = Menu(window)
window.config(menu=mainmenu)

TurtleSymbol = chr(9788)

TurtleCords = {"x": 0, "y": 0}

sizeX = 30
sizeY = 15

VisualMap = Label(window)

Map = list()

def createNewMap():
    global Map
    Map = []
    for _ in range(sizeY):
        Line = list()
        for _ in range(sizeX):
            Line.append(chr(9632))
        Map.append(Line)


def drawMap():
    global Map
    MapString = ""
    for Line in Map:
        for Symbol in Line:
            MapString = MapString + Symbol
        MapString += "\n"
    VisualMap.config(text=MapString)
    VisualMap.pack()


def placeTurtle():
    Map[TurtleCords["y"]][TurtleCords["x"]] = TurtleSymbol
    drawMap()

def Newgame():
    createNewMap()
    drawMap()
    placeTurtle()


menuFile = Menu(mainmenu, tearoff=0)
menuFile.add_command(label="Выход", command=lambda:exit(0))


menuGame = Menu(mainmenu, tearoff=0)
menuGame.add_command(label="Начать игру", command=Newgame)


menuAbout = Menu(mainmenu, tearoff=0)


mainmenu.add_cascade(label="Файл", menu=menuFile)
mainmenu.add_cascade(label="Игра", menu=menuGame)
mainmenu.add_cascade(label="О программе", menu=menuAbout)











window.mainloop()

