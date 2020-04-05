from tkinter import*
import random
import winsound
import math

window = Tk()
window.title("Черепашка и грибы")
window.geometry("800x600")
mainmenu = Menu(window)
window.config(menu=mainmenu)

gameEnded = False

TurtleSymbol = chr(81)
BackgroundSymbol = chr(9633)
MushroomSymbol = chr(0xB7)
ObstacleSymbol = chr(0xA1)
MoleSymbol = chr(0x69)

defObstacleCount = 5
ObstacleCount = 5
ObstacleCords = list()

defMushroomCount = 5
MushroomCount = 5
MushroomCords = list()

defMoleCount = 5
MoleCount = 5
MoleCords = list()

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



def OptionsOk(options, Y, X ,M, O, SM):
    global sizeY, sizeX, defMushroomCount, defObstacleCount, defMoleCount
    ErrorVidget = None
    try:
        sizeY = int(Y.get())
    except:
        ErrorVidget = Y
    try:
        sizeX = int(X.get())
    except:
        ErrorVidget = X
    try:
        defMushroomCount = int(M.get())
    except:
        ErrorVidget = M
    try:
        defMoleCount = int(SM.get())
    except:
        ErrorVidget = SM
    try:
        defObstacleCount = int(O.get())
    except:
        ErrorVidget = O
    if ErrorVidget != None:
        ErrorVidget.focus_set()
        ErrorWindow = Toplevel()
        ErrorWindow.title("Ошибка!!!")
        ErrorWindow.geometry("320x75")
        ErrorLabel = Label(ErrorWindow, text="Некоректные данные")
        ErrorLabel.pack()
        ErrorButton = Button(ErrorWindow, text="Ok", height=1, width=6)
        ErrorButton.bind("<Button-1>", lambda event: ErrorWindow.destroy())
        ErrorButton.pack()
        return
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

    ObstacleCountLabel = Label(options, text="Количество препятствий: ")
    ObstacleCountLabel.grid(row=3, column=0, sticky=W, padx=4, pady=2)
    ObstacleCountEntry = Entry(options)
    ObstacleCountEntry.grid(row=3, column=1, sticky=W, padx=4, pady=2)

    MoleCountLabel = Label(options, text="Количество саблезубых кротов: ")
    MoleCountLabel.grid(row=4, column=0, sticky=W, padx=4, pady=2)
    MoleCountEntry = Entry(options)
    MoleCountEntry.grid(row=4, column=1, sticky=W, padx=4, pady=2)

    OKbutton = Button(options, text="Ok", height=1, width=6)
    OKbutton.grid(row=5, column=0, sticky=E, padx=30)
    OKbutton.bind("<Button-1>", lambda event: OptionsOk(options, sizeYentry, sizeXentry, MushroomCountentry, ObstacleCountEntry, MoleCountEntry))

    Cancelbutton = Button(options, text="Cancel", height=1, width=6)
    Cancelbutton.grid(row=5, column=1, sticky=W, padx=30)
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
            elif isMole(x, y):
                Line.append(MoleSymbol)
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


def placeMole():
    global MoleCords, MoleCount
    MoleCords = list()
    MoleCount = defMoleCount
    for i in range(MoleCount):
        x = random.randint(0, sizeX - 1)
        y = random.randint(0, sizeY - 1)
        while not isAvaliableforMole(x, y):
            x = random.randint(0, sizeX - 1)
            y = random.randint(0, sizeY - 1)
        cords = [x, y]
        MoleCords.append(cords)

def placeMushrooms():
    global MushroomCords, MushroomCount
    MushroomCords = list()
    MushroomCount = defMushroomCount
    for i in range(MushroomCount):
        x = random.randint(0, sizeX - 1)
        y = random.randint(0, sizeY - 1)
        while not isAvaliableforMushroom(x, y):
            x = random.randint(0, sizeX - 1)
            y = random.randint(0, sizeY - 1)
        cords = [x, y]
        MushroomCords.append(cords)

def distanceToTurtle(x, y):
    global MoleCords, TurtleCordsX, TurtleCordsY
    return math.sqrt((TurtleCordsX - x) ** 2 + (TurtleCordsY - y) ** 2)


def isSurround(x, y):
    return isObstacleOrOut(x - 1, y) and isObstacleOrOut(x, y - 1) \
            and isObstacleOrOut(x + 1, y) and isObstacleOrOut(x, y + 1)

def isAvaliable(x, y):
    return isFree(x, y) and not isSurround(x, y)

def isAvaliableforMole(x, y):
    return isAvaliable(x, y) and distanceToTurtle(x, y) > 4

def isAvaliableforMushroom(x, y):
    return isAvaliable(x, y)

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

def isMole(x, y):
    for cord in (MoleCords):
        if cord[0] == x and cord[1] == y:
            return True
    return False

def isObstacleOrOut(x, y):
    return isObstacle(x, y) or x < 0 or y < 0 or x > sizeX or y > sizeY

def isFree(x, y):
    return not isMushroom(x, y) and not isTurtle(x, y) and not isObstacle(x, y) and not isMole(x, y)

def checkAndEat():
    global MushroomCount
    for i in range(len(MushroomCords)):
        cord = MushroomCords[i]
        if cord[0] == TurtleCordsX and cord[1] == TurtleCordsY:
            MushroomCount = MushroomCount - 1
            del MushroomCords[i]
            winsound.PlaySound("Niam.wav", winsound.SND_ASYNC + winsound.SND_PURGE)
            refreshMushroomCounter()
            if MushroomCount == 0:
                winsound.PlaySound("yraa.wav", winsound.SND_ASYNC + winsound.SND_PURGE)
                winGame()
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

def winGame():
    global gameEnded
    gameEnded = True
    loseGameWindow = Toplevel()
    loseGameWindow.title("Победа")
    loseGameWindow.geometry("300x80")
    loseGameLabel = Label(loseGameWindow, text="Вы выиграли")
    loseGameLabel.pack()
    CloseButton = Button(loseGameWindow, text="Закрыть")
    CloseButton.bind("<Button-1>", lambda event: loseGameWindow.destroy())
    CloseButton.pack()

def loseGame():
    global gameEnded
    gameEnded = True
    MushroomPicked = defMushroomCount - MushroomCount
    loseGameWindow = Toplevel()
    loseGameWindow.title("Поражение")
    loseGameWindow.geometry("300x80")
    loseGameLabel = Label(loseGameWindow, text="Вы проиграли")
    loseGameLabel.pack()
    MushroomLabel = Label(loseGameWindow, text="Собрано грибов: " + str(MushroomPicked))
    MushroomLabel.pack()
    CloseButton = Button(loseGameWindow, text="Закрыть")
    CloseButton.bind("<Button-1>", lambda event: loseGameWindow.destroy())
    CloseButton.pack()

def moveTurtle(direction):
    global TurtleCordsY, TurtleCordsX, gameEnded
    if gameEnded:
        return
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
    if isMole(TurtleCordsX, TurtleCordsY):
        winsound.PlaySound("aiaiai.wav", winsound.SND_ASYNC + winsound.SND_PURGE)
        loseGame()
        drawMap()
        return
    placeTurtle()
    checkAndEat()


def Newgame():
    global TurtleCordsY, TurtleCordsX, gameEnded
    gameEnded = False
    TurtleCordsX = sizeX // 2
    TurtleCordsY = sizeY // 2
    placeObstacles()
    placeMushrooms()
    placeMole()
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

