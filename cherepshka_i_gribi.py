from tkinter import*
import random
import winsound

window = Tk()
window.title("Черепашка и грибы")
window.geometry("800x600")
mainmenu = Menu(window)
window.config(menu=mainmenu)

TurtleSymbol = chr(81)
BackgroundSymbol = chr(9633)
MushroomSymbol = chr(0xB7)
ObstacleSymbol = chr(0xA1)

ObstacleCount = 5
defObstacleCount = 5
ObstacleCords = list()

defMushroomCount = 5
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



def OptionsOk(options, Y, X ,M):
    global sizeY, sizeX, defMushroomCount
    sizeY = int(Y.get())
    sizeX = int(X.get())
    defMushroomCount = int(M.get())
    options.destroy()


def SetOptions():
    options = Toplevel(window)
    options.title("Настройки игры")
    sizeYlabel = Label(options, text="Высота поля: ")
    sizeYlabel.grid(row=0, column=0, sticky=W, padx=4, pady=2)
    sizeYentry = Entry(options)
    sizeYentry.grid(row=0, column=1, sticky=W, padx=4, pady=2)

    sizeXlabel = Label(options, text="Ширина поля: ")
    sizeXlabel.grid(row=1, column=0, sticky=W, padx=4, pady=2)
    sizeXentry = Entry(options)
    sizeXentry.grid(row=1, column=1, sticky=W, padx=4, pady=2)

    MushroomCountLabel = Label(options, text="Количество грибов: ")
    MushroomCountLabel.grid(row=2, column=0, sticky=W, padx=4, pady=2)
    MushroomCountentry = Entry(options)
    MushroomCountentry.grid(row=2, column=1, sticky=W, padx=4, pady=2)

    OKbutton = Button(options, text="Ok", height=1, width=6)
    OKbutton.grid(row=3, column=0, sticky=E, padx=30)
    OKbutton.bind("<Button-1>", lambda event: OptionsOk(options, sizeYentry, sizeXentry, MushroomCountentry))

    Cancelbutton = Button(options, text="Cancel", height=1, width=6)
    Cancelbutton.grid(row=3, column=1, sticky=W, padx=30)
    Cancelbutton.bind("<Button-1>", lambda event: options.destroy())



def createNewMap():
    global Map
    Map = []
    for y in range(sizeY):
        Line = list()
        for x in range(sizeX):
            if isObstacle(x, y):
                Line.append(ObstacleSymbol)
            elif isMushroom(x, y):
                Line.append(MushroomSymbol)
            else:
                Line.append(BackgroundSymbol)
        Map.append(Line)


def drawMap():
    global Map
    MapString = ""
    for Line in Map:
        for Symbol in Line:
            MapString = MapString + Symbol
        MapString += "\n"
    VisualMap.config(text=MapString, font="Symbol 20")
    VisualMap.pack()
    print(ObstacleCords)

def placeTurtle():
    Map[TurtleCordsY][TurtleCordsX] = TurtleSymbol
    drawMap()


def placeObstacles():
    global ObstacleCords, ObstacleCount
    ObstacleCords = list()
    ObstacleCount = defObstacleCount
    for i in range(ObstacleCount):
        x = random.randint(0, sizeX - 1)
        y = random.randint(0, sizeY - 1)
        while not isFree(x, y):
            x = random.randint(0, sizeX - 1)
            y = random.randint(0, sizeY - 1)
        cords = [x, y]
        ObstacleCords.append(cords)


def placeMushrooms():
    global MushroomCords, MushroomCount
    MushroomCords = list()
    MushroomCount = defMushroomCount
    for i in range(MushroomCount):
        x = random.randint(0, sizeX - 1)
        y = random.randint(0, sizeY - 1)
        while not isFree(x, y):
            x = random.randint(0, sizeX - 1)
            y = random.randint(0, sizeY - 1)
        cords = [x, y]
        MushroomCords.append(cords)



def refreshMushroomCounter():
    VisualMushroomCount.config(text="Осталось грибов: " + str(MushroomCount))
    VisualMushroomCount.pack()

def isTurtle(x, y):
    return x == TurtleCordsX and y == TurtleCordsY

def isMushroom(x, y):
    for cord in (MushroomCords):
        if cord[0] == x and cord[1] == y:
            return True
    return False

def isObstacle(x, y):
    for cord in (ObstacleCords):
        if cord[0] == x and cord[1] == y:
            return True
    return False

def isFree(x, y):
    return not isMushroom(x, y) and not isTurtle(x, y) and not isObstacle(x, y)

def checkAndEat():
    global MushroomCount
    for i in range(len(MushroomCords)):
        cord = MushroomCords[i]
        if cord[0] == TurtleCordsX and cord[1] == TurtleCordsY:
            MushroomCount = MushroomCount - 1
            del MushroomCords[i]

            winsound.PlaySound("Niam.wav", winsound.SND_ASYNC + winsound.SND_PURGE)
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
    CordY = TurtleCordsY
    CordX = TurtleCordsX
    if direction == Up:
        CordY = max(TurtleCordsY - 1, 0)
    if direction == Left:
        CordX = max(TurtleCordsX - 1, 0)
    if direction == Down:
        CordY = min(TurtleCordsY + 1, sizeY - 1)
    if direction == Right:
        CordX = min(TurtleCordsX + 1, sizeX - 1)
    if isObstacle(CordX, CordY):
        return
    Map[TurtleCordsY][TurtleCordsX] = BackgroundSymbol
    TurtleCordsY = CordY
    TurtleCordsX = CordX
    placeTurtle()
    checkAndEat()


def Newgame():
    global TurtleCordsY, TurtleCordsX
    TurtleCordsX = sizeX // 2
    TurtleCordsY = sizeY // 2
    placeObstacles()
    placeMushrooms()
    createNewMap()
    drawMap()
    refreshMushroomCounter()
    placeTurtle()

menuFile = Menu(mainmenu, tearoff=0)
menuFile.add_command(label="Выход", command=lambda: exit(0))

menuGame = Menu(mainmenu, tearoff=0)
menuGame.add_command(label="Начать игру", command=Newgame)
menuGame.add_command(label="Настройки", command=SetOptions)

menuAbout = Menu(mainmenu, tearoff=0)

mainmenu.add_cascade(label="Файл", menu=menuFile)
mainmenu.add_cascade(label="Игра", menu=menuGame)
mainmenu.add_cascade(label="О программе", menu=menuAbout)

window.bind("<Key>", KeyPress)

window.mainloop()

