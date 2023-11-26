# TODO
# Prototypes
# [x] Single line printing prototype
# [x] Multi line printing prototype
# [x] Continuous printing prototype
# [x] Delete lines prototype
# [x] Typing prototype
# [x] Scrolling prototype
# Implementations
# [x] Blinking cursor
# [x] Delete lines
# [x] Scrolling
# [x] Typing simulation w/ speed
# [] Merge genText() and genMultiText()
# [] Fix n then (n + 1) print config
# [] Prompt
# [] Realistic scrolling
# [] Need cloneFrame() and replaceText() ?
# [] Optimization + better code quality
# [] Config file
# [] Theming
# [] Scriptable input file
# [] Remove debug statements
# [] GIF maker implementation

from PIL import Image, ImageDraw, ImageFont
import random
from icecream import ic
import os  # debug

os.system("rm -fr frame* output*")  # debug

width, height = 640, 480  # VGA
fontFile = "gohufont-uni-14.pil"
bgColor = "#181825"
txtColor = "#cdd6f4"
baseName = "frame_"
folderName = "./frames/"
os.mkdir(folderName)
fps = 8.0

frameCount = 0
xPad, yPad = 15, 15
currRow = 0
currCol = 0

font = ImageFont.load(fontFile)  # bitmap monospaced font
fontWidth, fontHeight = font.getbbox("W")[2], font.getbbox("H")[3]
lineSpacing = 4  # default

numRows = (height - 2 * yPad) // (fontHeight + lineSpacing)
numCols = (width - 2 * xPad) // (fontWidth)
# ic(numRows, numCols)  # debug

cursor = "_"
cursorOrig = cursor
showCursor = True


def alterCursor():
    global cursor
    if cursor is cursorOrig:
        cursor = " "
    else:
        cursor = cursorOrig
    ic("alterCursor():", cursor)  # debug


def genFrame(frame: Image.Image = None) -> Image.Image:
    global frameCount, colInRow
    if frame is None:
        frame = Image.new("RGB", (width, height), bgColor)
        colInRow = {_ + 1: 1 for _ in range(numRows)}
        # checker box to debug
        # draw = ImageDraw.Draw(frame)
        # for i in range(numRows + 1):  # (n + 1) lines
        #     x1 = xPad
        #     x2 = width - xPad
        #     y1 = y2 = yPad + i * (fontHeight + lineSpacing)
        #     draw.line([(x1, y1), (x2, y2)], "yellow")
        # for i in range(numCols + 1):  # (n + 1) lines
        #     x1 = x2 = xPad + i * fontWidth
        #     y1 = yPad
        #     y2 = height - yPad
        #     draw.line([(x1, y1), (x2, y2)], "turquoise")
        # draw.line([(xPad, yPad), (width - xPad, yPad)], "red")  # top
        # draw.line([(xPad, yPad), (xPad, height - yPad)], "red")  # left
        # draw.line(
        #     [(xPad, height - yPad), (width - xPad, height - yPad)], "red"
        # )  # bottom
        # draw.line([(width - xPad, yPad), (width - xPad, height - yPad)], "red")  # right
        cursorToBox(1, 1)  # initialize at box (1, 1)
        return frame

    frameCount += 1
    ic("genFrame():", frameCount)  # debug
    fileName = baseName + str(frameCount) + ".png"
    frame.save(folderName + fileName, "PNG")
    return frame


def cloneFrame(frame: Image.Image, count: int = 1) -> Image.Image:
    for _ in range(count):
        frame = genFrame(frame)
    return frame


def getCoords(rowNum: int, colNum: int) -> tuple:
    x1 = xPad + (colNum - 1) * fontWidth
    y1 = yPad + (rowNum - 1) * (fontHeight + lineSpacing)
    x2 = xPad + colNum * fontWidth
    y2 = yPad + rowNum * (fontHeight + lineSpacing)
    return x1, y1, x2, y2


def cursorToBox(
    rowNum: int,
    colNum: int,
    textNumLines: int = 1,
    textNumChars: int = 1,
    contin: bool = False,
) -> tuple:
    if rowNum < 1 or colNum < 1 or rowNum > numRows or colNum > numCols:
        raise ValueError
    global currRow, currCol
    maxRowNum = numRows - textNumLines + 1
    maxColNum = numCols - textNumChars + 1
    minColNum = colInRow[rowNum]
    if colNum > maxColNum:
        ic(
            "cursorToBox():",
            textNumChars,
            "chars cannot be accomodated at column",
            colNum,
        )
    if rowNum > maxRowNum:
        ic("cursorToBox():", textNumLines, "lines cannot be accomodated at row", rowNum)
        ic("cursorToBox():", "need minimum rowNum", maxRowNum)
        rowNum = maxRowNum
        # exit(1) # debug

    if contin is False and colInRow[rowNum] != 1:
        scrollTimes = textNumLines
        scrollUp(scrollTimes)
        colNum = 1
    elif contin is True:
        if colNum < minColNum:
            ic(
                "cursorToBox():",
                textNumChars,
                "chars cannot be accomodated at column",
                colNum,
            )
            colNum = colInRow[rowNum]
    currRow, currCol = rowNum, colNum
    ic("cursorToBox():", currRow, currCol)  # debug
    return getCoords(rowNum, colNum)


def genText(
    text: str, rowNum: int, colNum: int, count: int = 1, contin: bool = False
) -> None:
    global frame, currRow, currCol, colInRow
    textNumLines = len(text.splitlines())
    if textNumLines > 1:
        ic("genText():", "Not for multiline texts")  # debug
    else:
        textNumChars = len(text)
        x1, y1, _, _ = cursorToBox(rowNum, colNum, 1, textNumChars, contin)
        draw = ImageDraw.Draw(frame)
        draw.text((x1, y1), text, txtColor, font)
        currCol += len(text)
        colInRow[currRow] = currCol
        # if currRow != numRows: currRow += 1; currCol = colInRow[currRow] # end up cursor one line below
        ic("genText():", currRow, currCol, colInRow)  # debug

        for _ in range(count):
            if showCursor:
                cx1, cy1, _, _ = cursorToBox(
                    currRow, currCol, 1, 1, contin=True
                )  # no unnecessary scroll
                draw.text((cx1, cy1), cursor, txtColor, font)
            genFrame(frame)
            if showCursor:
                blankBoxImage = Image.new(
                    "RGB", (fontWidth, fontHeight + lineSpacing), bgColor
                )
                frame.paste(blankBoxImage, (cx1, cy1))
                alterCursor()


def genMultiText(
    text: str | list, rowNum: int, colNum: int, count: int = 1, contin: bool = False
) -> None:
    global frame, currRow, currCol, colInRow
    if isinstance(text, str):
        textLines = text.splitlines()
        textNumLines = len(textLines)
    else:
        textLines = text
        textNumLines = len(text)
    if textNumLines == 1:
        ic("genMultiText():", "Not for single line texts")  # debug
    else:
        cursorToBox(
            rowNum, colNum, textNumLines, 1, contin
        )  # initialize cursor at correct scrolled position
        for line in textLines:
            textNumChars = len(line)
            x1, y1, _, _ = cursorToBox(currRow, colNum, 1, textNumChars, contin)
            draw = ImageDraw.Draw(frame)
            draw.text((x1, y1), line, txtColor, font)
            currCol += len(line)
            colInRow[currRow] = currCol
            if currRow != numRows:
                currRow += 1  # end up cursor one line below
                currCol = colInRow[currRow]
                # rowNum = currRow # new rowNum for next iteration
            ic("genMultiText():", currRow, currCol, colInRow)  # debug

        for _ in range(count):
            if showCursor:
                cx1, cy1, _, _ = cursorToBox(
                    currRow, currCol, 1, 1, contin=True
                )  # no unnecessary scroll
                draw.text((cx1, cy1), cursor, txtColor, font)
            genFrame(frame)
            if showCursor:
                blankBoxImage = Image.new(
                    "RGB", (fontWidth, fontHeight + lineSpacing), bgColor
                )
                frame.paste(blankBoxImage, (cx1, cy1))
                alterCursor()


# def replaceText(text: str, rowNum: int, colNum: int, count: int = 1) -> None:
#     global frame
#     chars = 0
#     for _ in text:
#         chars += 1
#     layerImage = Image.new(
#         "RGB", (chars * fontWidth, fontHeight + lineSpacing), bgColor
#     )
#     x1, y1, _, _ = cursorToBox(rowNum, colNum)
#     frame.paste(layerImage, (x1, y1))
#     genText(text, rowNum, colNum, count)


def genTypingText(
    text: str, rowNum: int, colNum: int, contin: bool = False, speed: int = 0
) -> None:
    # speed configuration
    # 0 - random - random frames
    # 1 - fast - 1 frames
    # 2 - medium - 2 frames
    # 3 - slow - 3 frames
    if contin is False:
        cursorToBox(rowNum, colNum, 1, 1, contin)
    if speed == 1 or speed == 2 or speed == 3:
        for char in text:
            genText(char, rowNum, currCol, True, speed)
    else:
        for char in text:
            count = random.choice([1, 2, 3])
            genText(char, rowNum, currCol, True, count)


def scrollUp(count: int = 1) -> None:
    global frame, currRow, currCol, colInRow
    for _ in range(count):
        croppedFrame = frame.crop(
            (0, fontHeight + lineSpacing, width, height)
        )  # make room for 1 extra line (fontHeight + lineSpacing)
        frame = Image.new("RGB", (width, height), bgColor)
        frame.paste(croppedFrame, (0, 0))
        # currCol = colInRow[currRow] # useless as currCol is shifted up
        currRow -= 1  # move cursor to where it was

        keys = list(colInRow.keys())
        values = list(colInRow.values())
        shiftedValues = values[1:] + [1]
        shiftedDict = dict(zip(keys, shiftedValues))
        colInRow = shiftedDict
        ic("scrollUp():", currRow, currCol, colInRow)


def deleteRow(rowNum: int) -> None:
    global frame, colInRow
    _, y1, _, _ = cursorToBox(
        rowNum, 1, 1, 1, True
    )  # continue = True; do not scroll up
    colInRow[rowNum] = 1
    blankLineImage = Image.new("RGB", (width - xPad, fontHeight + lineSpacing), bgColor)
    frame.paste(blankLineImage, (0, y1))


# TEST BED
showCursor = False
frame = genFrame(None)  # initial blank frame
genText("", 1, 1, False, 5)
genText("Starting GIF OS ", 1, 1, 5, False)
genTypingText(".....", 1, 1, True)
for i in range(0x0, 0x40000000, 0x7FFFFFF):
    deleteRow(2)
    genText("Memory Check: {}".format(i), 2, 1)
cloneFrame(frame, 5)
deleteRow(2)
genText("Memory Check: 1048576KB OK", 2, 1, 5)

showCursor = True
frame = genFrame(None)
genText("", 1, 1, 5)
showCursor = False
genText("Enter username: ", 1, 1, 5)
showCursor = True
genTypingText("x0rzavi", 1, 1, True)
cloneFrame(frame, 5)
showCursor = True
genText("", 2, 1, 5)
showCursor = False
genText("Enter password: ", 2, 1, 5)
showCursor = True
genTypingText("*********", 2, 1, True)
genText("", 3, 1, 5)
genText("Coded by x0rzavi :D", numRows, 1, 10)
cloneFrame(frame, 2)

# frame = genFrame(None)
# genMultiText("github-terminal-magic on main\n$> ", 1, 1, 5)
# genTypingText("fastfetch", 2, 1, True)
# multiLines1 = """                  -`                     x0rzavi@WIN-X0RZAVI
#                  .o+`                    -------------------
#                 `ooo/                    OS: Arch Linux x86_64
#                `+oooo:                   Host: Windows Subsystem for Linux - Arch
#               `+oooooo:                  Kernel: 5.15.133.1-microsoft-standard-WSL2
#               -+oooooo+:                 Uptime: 12 hours, 2 mins
#             `/:-:++oooo+:                Packages: 503 (pacman)
#            `/++++/+++++++:               Shell: zsh 5.9
#           `/++++++++++++++:              Display (westonrdp): 1920x1080 @ 60Hz
#          `/+++ooooooooooooo/`            WM: WSLg (Wayland)
#         ./ooosssso++osssssso+`           Terminal: tmux 3.3a
#        .oossssso-````/ossssss+`          CPU: AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx (8) @ 2.10 GHz
#       -osssssso.      :ssssssso.         GPU: AMD Radeon(TM) Vega 8 Graphics (1.99 GiB) [Integrated]
#      :osssssss/        osssso+++.        Memory: 1.12 GiB / 6.75 GiB (17%)
#     /ossssssss/        +ssssooo/-        Swap: 0 B / 2.00 GiB (0%)
#   `/ossssso+/:-        -:/+osssso+-      Disk (/): 5.00 GiB / 1006.85 GiB (0%) - ext4
#  `+sso+:-`                 `.-/+oso:     Disk (/mnt/c): 85.88 GiB / 200.75 GiB (43%) - 9p
# `++:.                           `-/+/    Disk (/mnt/d): 224.03 GiB / 931.50 GiB (24%) - 9p
# .`                                 `/    Local IP (eth0): 172.22.214.187/20 *
#                                          Battery: 100% [Full]
#                                          Locale: en_US.UTF-8"""
# genText(multiLines1, currRow, 15)

# genText("github-terminal-magic on main\n$> ", currRow, 15)
# genText(multiLines1 + "\ngithub-terminal-magic on main\n$> ", 3, 15)
# genTypingText("ll -p", currRow, True)
# multiLines2 = """total 176K
# drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Nov 19 00:10 frames/
# drwxr-xr-x 8 x0rzavi x0rzavi 4.0K Nov 18 22:22 .git/
# -rw-r--r-- 1 x0rzavi x0rzavi 3.1K Nov 18 15:20 .gitignore
# -rw-r--r-- 1 x0rzavi x0rzavi 106K Nov 17 12:10 gohufont-uni-14.bdf
# -rw-r--r-- 1 x0rzavi x0rzavi 1.3K Nov 17 12:10 gohufont-uni-14.pbm
# -rw-r--r-- 1 x0rzavi x0rzavi 5.1K Nov 17 12:10 gohufont-uni-14.pil
# -rw-r--r-- 1 x0rzavi x0rzavi 1.1K Nov 17 11:51 LICENSE
# -rw-r--r-- 1 x0rzavi x0rzavi 7.9K Nov 19 00:13 main.py"""
# genText(multiLines2, currRow, 1)
# multiLines3 = """drwxr-xr-x 3 x0rzavi x0rzavi 4.0K Nov 18 21:35 .mypy_cache/
# -rw-r--r-- 1 x0rzavi x0rzavi  20K Nov 19 00:10 output.gif
# -rw-r--r-- 1 x0rzavi x0rzavi  511 Nov 18 21:01 temp.py
# drwxr-xr-x 5 x0rzavi x0rzavi 4.0K Nov 17 12:05 venv/"""
# genText(multiLines3, currRow, 15)

os.system(
    "ffmpeg -hide_banner -loglevel error -r {fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif".format(
        fps=fps, folderName=folderName
    )
)  # debug
