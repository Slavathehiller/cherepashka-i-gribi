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

defMoleCount = 1
MoleCount = 1
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

def ShowError(ErrorText, vidget = None):
    ErrorWindow = Toplevel()
    ErrorWindow.title("ОШИБКА")
    ErrorWindow.geometry("300x60")
    Errorlabel = Label(ErrorWindow, text=ErrorText)
    Errorlabel.pack()
    ErrorButton = Button(ErrorWindow, text="Ok")
    ErrorButton.bind("<Button-1>", lambda event: ErrorWindow.destroy())
    ErrorButton.pack()
    if vidget != None:
        vidget.focus_set()

def OptionsOk(options, Y, X ,M, O, SM):
    global sizeY, sizeX, defMushroomCount, defObstacleCount, defMoleCount
    cordY = 0
    cordX = 1
    obst = 2
    moles = 3
    mush = 4
    IntValues = []
    for vidget in [Y, X, O, SM, M]:
        try:
            IntValues.append(int(vidget.get()))
        except:
            ShowError("Некоректные данные", vidget)
            return
    if IntValues[cordY] > 30:
        ShowError("Высота поля должна быть не более 30 клеток", Y)
        return

    if IntValues[cordX] > 100:
        ShowError("Ширина поля должна быть не более 100 клеток", X)
        return

    defOC = IntValues[cordY] * IntValues[cordX] // 10
    if IntValues[obst] > defOC:
        ShowError("Количество препятствий должно быть не более " + str(defOC), O)
        return

    defSM = IntValues[cordY] * IntValues[cordX] // 10
    if IntValues[moles] > defSM:
        ShowError("Количество кротов должно быть не более " + str(defSM), SM)
        return

    defMC = IntValues[cordY] * IntValues[cordX] // 20
    if IntValues[mush] > defMC:
        ShowError("Количество грибов должно быть не более " + str(defMC), M)
        return
    if IntValues[mush] < 1:
        ShowError("Количество грибов должно быть больше 0 ", M)
        return

    sizeY = IntValues[cordY]
    sizeX = IntValues[cordX]
    defObstacleCount = IntValues[obst]
    defMushroomCount = IntValues[mush]
    defMoleCount = IntValues[moles]
    options.destroy()


def SetOptions():
    sizeYVar = StringVar()
    sizeXVar = StringVar()
    MushroomVar = StringVar()
    ObstacleVar = StringVar()
    MoleVar = StringVar()

    options = Toplevel(window)
    options.geometry("350x170")
    options.title("Настройки игры")
    sizeYlabel = Label(options, text="Высота поля: ")
    sizeYlabel.grid(row=0, column=0, sticky=W, padx=4, pady=2)
    sizeYentry = Entry(options, textvariable=sizeYVar)
    sizeYVar.set(sizeY)
    sizeYentry.grid(row=0, column=1, sticky=W, padx=4, pady=2)

    sizeXlabel = Label(options, text="Ширина поля: ")
    sizeXlabel.grid(row=1, column=0, sticky=W, padx=4, pady=2)
    sizeXentry = Entry(options, textvariable=sizeXVar)
    sizeXVar.set(sizeX)
    sizeXentry.grid(row=1, column=1, sticky=W, padx=4, pady=2)

    MushroomCountLabel = Label(options, text="Количество грибов: ")
    MushroomCountLabel.grid(row=2, column=0, sticky=W, padx=4, pady=2)
    MushroomCountentry = Entry(options, textvariable=MushroomVar)
    MushroomVar.set(MushroomCount)
    MushroomCountentry.grid(row=2, column=1, sticky=W, padx=4, pady=2)

    ObstacleCountLabel = Label(options, text="Количество препятствий: ")
    ObstacleCountLabel.grid(row=3, column=0, sticky=W, padx=4, pady=2)
    ObstacleCountEntry = Entry(options, textvariable=ObstacleVar)
    ObstacleVar.set(ObstacleCount)
    ObstacleCountEntry.grid(row=3, column=1, sticky=W, padx=4, pady=2)

    MoleCountLabel = Label(options, text="Количество саблезубых кротов: ")
    MoleCountLabel.grid(row=4, column=0, sticky=W, padx=4, pady=2)
    MoleCountEntry = Entry(options, textvariable=MoleVar)
    MoleVar.set(MoleCount)
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
    minDistance = min(sizeY * sizeX // 25, 4)
    return isAvaliable(x, y) and distanceToTurtle(x, y) > minDistance

def isAvaliableforMushroom(x, y):
    return isAvaliable(x, y)

def moleCanMoveTo(x, y):
    return (isFree(x, y) or isTurtle(x, y)) and not isOut(x, y)

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

def isOut(x, y):
    return x < 0 or y < 0 or x > sizeX - 1 or y > sizeY - 1

def isObstacleOrOut(x, y):
    return isObstacle(x, y) or isOut(x, y)

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
    winsound.PlaySound("aiaiai.wav", winsound.SND_ASYNC + winsound.SND_PURGE)
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


def moveMole(mole, direction):
    global MoleCords
    X = MoleCords[mole][0]
    Y = MoleCords[mole][1]
    if direction == Up:
        Y = Y - 1
    if direction == Left:
        X = X - 1
    if direction == Down:
        Y = Y + 1
    if direction == Right:
        X = X + 1
    if moleCanMoveTo(X, Y):
        Map[MoleCords[mole][1]][MoleCords[mole][0]] = BackgroundSymbol
        MoleCords[mole][0] = X
        MoleCords[mole][1] = Y
        Map[Y][X] = MoleSymbol
        drawMap()
    if isTurtle(X, Y):
        loseGame()

def moveAllMoles():
    for i in range(0, MoleCount):
        moveMole(i, random.randint(1, 4))

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
        loseGame()
        drawMap()
        return
    placeTurtle()
    checkAndEat()
    moveAllMoles()


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

