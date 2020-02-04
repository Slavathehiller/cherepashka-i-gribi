from tkinter import*
import random

window = Tk()
window.title("Черепашка и грибы")
window.geometry("800x600")
mainmenu = Menu(window)
window.config(menu=mainmenu)

TurtleSymbol = chr(164)
BackgroundSymbol = chr(9633)
MushroomSymbol = chr(84)

MushroomCount = 5
MushroomCords = list()

sizeX = 10
sizeY = 5

TurtleCordsX = sizeX // 2
TurtleCordsY = sizeY // 2

Up = 1
Down = 2
Left = 3
Right = 4

VisualMushroomCount = Label(window, text="Осталось грибов: " + str(MushroomCount))

VisualMap = Label(window)

Map = list()


def createNewMap():
    global Map
    Map = []
    for _ in range(sizeY):
        Line = list()
        for _ in range(sizeX):
            Line.append(BackgroundSymbol)
        Map.append(Line)


def drawMap():
    global Map
    MapString = ""
    for Line in Map:
        for Symbol in Line:
            MapString = MapString + Symbol
        MapString += "\n"
    VisualMap.config(text=MapString, font="terminal 20")
    VisualMap.pack()


def placeTurtle():
    Map[TurtleCordsY][TurtleCordsX] = TurtleSymbol
    drawMap()


def placeMushrooms():
    for i in range(MushroomCount):
        global MushroomCords
        x, y = 0, 0
        while isMushroom(x, y):
            x = random.randint(0, sizeX - 1)
            y = random.randint(0, sizeY - 1)
        cords = [x, y]
        MushroomCords.append(cords)
        Map[y][x] = MushroomSymbol
    drawMap()



def refreshMushroomCounter():
    VisualMushroomCount.config(text="Осталось грибов: " + str(MushroomCount))
    VisualMushroomCount.pack()

def isMushroom(x, y):
    for cord in (MushroomCords):
        if cord[0] == x and cord[1] == y:
            return True
    return False

def checkAndEat():
    global MushroomCount
    for i in range(len(MushroomCords)):
        cord = MushroomCords[i]
        if cord[0] == TurtleCordsX and cord[1] == TurtleCordsY:
            MushroomCount = MushroomCount - 1
            del MushroomCords[i]
            refreshMushroomCounter()
            return


def KeyPress(event):
    if event.keycode == 38:
        moveTurtle(Up)
    elif event.keycode == 37:
        moveTurtle(Left)
    elif event.keycode == 40:
        moveTurtle(Down)
    elif event.keycode == 39:
        moveTurtle(Right)


def moveTurtle(direction):
    global TurtleCordsY, TurtleCordsX
    Map[TurtleCordsY][TurtleCordsX] = BackgroundSymbol
    if direction == Up:
        TurtleCordsY = max(TurtleCordsY - 1, 0)
    if direction == Left:
        TurtleCordsX = max(TurtleCordsX - 1, 0)
    if direction == Down:
        TurtleCordsY = min(TurtleCordsY + 1, sizeY - 1)
    if direction == Right:
        TurtleCordsX = min(TurtleCordsX + 1, sizeX - 1)
    placeTurtle()
    checkAndEat()


def Newgame():
    createNewMap()
    drawMap()
    placeMushrooms()
    refreshMushroomCounter()
    placeTurtle()

menuFile = Menu(mainmenu, tearoff=0)
menuFile.add_command(label="Выход", command=lambda: exit(0))


menuGame = Menu(mainmenu, tearoff=0)
menuGame.add_command(label="Начать игру", command=Newgame)


menuAbout = Menu(mainmenu, tearoff=0)


mainmenu.add_cascade(label="Файл", menu=menuFile)
mainmenu.add_cascade(label="Игра", menu=menuGame)
mainmenu.add_cascade(label="О программе", menu=menuAbout)

window.bind("<Key>", KeyPress)









window.mainloop()

