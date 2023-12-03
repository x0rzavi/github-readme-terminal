# TODO
# [x] Try not to manipulate currRow manually
# [] Optimization + better code quality - classes
# [] Need cloneFrame() and replaceText() ?
# [] Merge genText() and genMultiText()
# [] Config file
# [] Theming
# [] Scriptable input file
# [] Remove debug statements/optional debug mode
# [] GIF maker implementation
# [] Test cases

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
colInRow = {_ + 1: 1 for _ in range(numRows)}
# ic(numRows, numCols, colInRow)  # debug

cursor = "_"
cursorOrig = cursor
showCursor = True


def alterCursor():
    global cursor
    cursor = cursorOrig if cursor != cursorOrig else " "
    ic("alterCursor():", cursor)  # debug


def toggleShowCursor(choice: bool = None):
    global showCursor
    showCursor = not showCursor if choice is None else choice
    ic("toggleShowCursor():", showCursor)  # debug


def frameDebugLines(frame: Image.Image) -> Image.Image:
    # checker box to debug
    draw = ImageDraw.Draw(frame)
    for i in range(numRows + 1):  # (n + 1) lines
        x1 = xPad
        x2 = width - xPad
        y1 = y2 = yPad + i * (fontHeight + lineSpacing)
        draw.line([(x1, y1), (x2, y2)], "yellow")
        draw.text((0, y1), str(i + 1), "orange", font)  # row numbers
    for i in range(numCols + 1):  # (n + 1) lines
        x1 = x2 = xPad + i * fontWidth
        y1 = yPad
        y2 = height - yPad
        draw.line([(x1, y1), (x2, y2)], "turquoise")
    draw.line([(xPad, yPad), (width - xPad, yPad)], "red")  # top
    draw.line([(xPad, yPad), (xPad, height - yPad)], "red")  # left
    draw.line([(xPad, height - yPad), (width - xPad, height - yPad)], "red")  # bottom
    draw.line([(width - xPad, yPad), (width - xPad, height - yPad)], "red")  # right
    return frame


def genFrame(frame: Image.Image = None) -> Image.Image:
    global frameCount, colInRow
    if frame is None:
        frame = Image.new("RGB", (width, height), bgColor)
        colInRow = {_ + 1: 1 for _ in range(numRows)}
        # frame = frameDebugLines(frame)
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


def cursorToBox(
    rowNum: int,
    colNum: int,
    textNumLines: int = 1,
    textNumChars: int = 1,
    contin: bool = False,
) -> tuple:
    if rowNum < 1 or colNum < 1 or colNum > numCols:
        raise ValueError
    elif rowNum > numRows:
        ic("cursorToBox():", "rowNum exceeds max row number, using", numRows, "instead")
        rowNum = numRows
    global currRow, currCol
    maxRowNum = numRows - textNumLines + 1  # maximum row that can be permitted
    minColNum = colInRow[rowNum]

    if contin is False:
        numBlankRows = 0
        firstBlankRow = numRows + 1  # all rows are filled
        for i in range(numRows, rowNum - 1, -1):
            if colInRow[i] == 1:
                firstBlankRow = i
                numBlankRows += 1
            else:
                break
        ic("cursorToBox():", firstBlankRow, numBlankRows)

        if rowNum > maxRowNum:
            ic("cursorToBox():", textNumLines, "cannot be accomodated at", rowNum)
            ic("cursorToBox():", "maximum possible", maxRowNum)
            if firstBlankRow < maxRowNum:  # needed ?????
                ic("NEEDED!") # debug
                exit(1)
                scrollTimes = textNumLines - numBlankRows
                ic("cursorToBox():", scrollTimes)
                scrollUp(scrollTimes)
                rowNum = currRow
            else:
                rowNum = maxRowNum  # enough space to print; no need to scroll

        elif firstBlankRow > rowNum:
            scrollTimes = firstBlankRow - rowNum
            ic("cursorToBox():", scrollTimes)
            scrollUp(scrollTimes)
    else:
        if colNum < minColNum:
            ic(
                "cursorToBox():",
                textNumChars,
                "cannot be accomodated at",
                colNum,
            )
            colNum = colInRow[rowNum]
    currRow, currCol = rowNum, colNum
    ic("cursorToBox():", currRow, currCol)  # debug

    x1 = xPad + (colNum - 1) * fontWidth
    y1 = yPad + (rowNum - 1) * (fontHeight + lineSpacing)
    x2 = xPad + colNum * fontWidth
    y2 = yPad + rowNum * (fontHeight + lineSpacing)
    return x1, y1, x2, y2


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
        ic("genText():", currRow, currCol)  # debug

        for _ in range(count):
            if showCursor:
                cx1, cy1, _, _ = cursorToBox(
                    currRow, currCol, 1, 1, contin=True
                )  # no unnecessary scroll
                draw.text((cx1, cy1), str(cursor), txtColor, font)
            genFrame(frame)
            if showCursor:
                blankBoxImage = Image.new(
                    "RGB", (fontWidth, fontHeight + lineSpacing), bgColor
                )
                frame.paste(blankBoxImage, (cx1, cy1))
                alterCursor()


def genMultiText(
    text: str | list,
    rowNum: int,
    colNum: int,
    count: int = 1,
    prompt: bool = True,
    contin: bool = False,
) -> None:
    if prompt and contin:
        ic("genMultiText():", "both prompt and contin can't be True")  # debug
        exit(1)

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
        for i in range(textNumLines):
            line = textLines[i]
            textNumChars = len(line)
            x1, y1, _, _ = cursorToBox(rowNum + i, colNum, 1, textNumChars, contin)
            draw = ImageDraw.Draw(frame)
            draw.text((x1, y1), line, txtColor, font)
            currCol += len(line)
            colInRow[currRow] = currCol
            ic("genMultiText():", currRow, currCol)  # debug

        if prompt:
            cloneFrame(frame, 1)  # wait a bit before printing new prompt
            genPrompt(currRow + 1, 1, 1)  # next to currRow

        for _ in range(count):
            if showCursor:
                cx1, cy1, _, _ = cursorToBox(
                    currRow, currCol, 1, 1, contin=True
                )  # no unnecessary scroll
                draw.text((cx1, cy1), str(cursor), txtColor, font)
            genFrame(frame)
            if showCursor:
                blankBoxImage = Image.new(
                    "RGB", (fontWidth, fontHeight + lineSpacing), bgColor
                )
                frame.paste(blankBoxImage, (cx1, cy1))
                alterCursor()


def genPrompt(rowNum: int, colNum: int, count: int = 1):
    global showCursor
    origCursorState = showCursor
    toggleShowCursor(True)
    genText("x0rzavi@github ~> ", rowNum, colNum, count, False)
    showCursor = origCursorState


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
            genText(char, rowNum, colInRow[rowNum], speed, True)
    else:
        for char in text:
            count = random.choice([1, 2, 3])
            genText(char, rowNum, colInRow[rowNum], count, True)


def scrollUp(count: int = 1) -> None:
    global frame, currRow, currCol, colInRow
    for _ in range(count):
        croppedFrame = frame.crop(
            (0, fontHeight + lineSpacing, width, height)
        )  # make room for 1 extra line (fontHeight + lineSpacing)
        frame = Image.new("RGB", (width, height), bgColor)
        frame.paste(croppedFrame, (0, 0))
        currRow -= 1  # move cursor to where it was

        keys = list(colInRow.keys())
        values = list(colInRow.values())
        shiftedValues = values[1:] + [1]
        shiftedDict = dict(zip(keys, shiftedValues))
        colInRow = shiftedDict
        ic("scrollUp():", currRow, currCol)


def deleteRow(rowNum: int) -> None:
    global frame, colInRow
    _, y1, _, _ = cursorToBox(
        rowNum, 1, 1, 1, True
    )  # continue = True; do not scroll up
    colInRow[rowNum] = 1
    blankLineImage = Image.new("RGB", (width - xPad, fontHeight + lineSpacing), bgColor)
    frame.paste(blankLineImage, (0, y1))


## TEST BED
# toggleShowCursor(False)
# frame = genFrame(None)  # initial blank frame
# genText("", 1, 1, 5, False)
# genText("Starting GIF OS ", 1, 1, 5, False)
# genTypingText(".....", 1, 1, True)
# for i in range(0x0, 0x40000000, 0x7FFFFFF):
#     if i < 0x20000000:
#         cloneFrame(frame, 2)
#     deleteRow(2)
#     genText(f"Memory Check: {i}", 2, 1)
# cloneFrame(frame, 5)
# deleteRow(2)
# genText("Memory Check: 1048576KB OK", 2, 1, 5)
#
# toggleShowCursor(True)
# showCursor = True
# frame = genFrame(None)
# genText("", 1, 1, 5)
# toggleShowCursor(False)
# genText("Enter username: ", 1, 1, 5)
# toggleShowCursor(True)
# genTypingText("x0rzavi", 1, 1, True)
# cloneFrame(frame, 5)
# toggleShowCursor(True)
# genText("", 2, 1, 5)
# toggleShowCursor(False)
# genText("Enter password: ", 2, 1, 5)
# toggleShowCursor(True)
# genTypingText("*********", 2, 1, True)
# genText("", 3, 1, 5)
# genText("Coded by x0rzavi :D", numRows, 1, 10)
# cloneFrame(frame, 2)
#
# frame = genFrame(None)
# toggleShowCursor(True)
# genPrompt(1, 1, 1)
# genTypingText("fastfetch", 1, 1, True, 1)
# genText("", currRow + 1, 1, 1)
# lines1 = """                  -`                     x0rzavi@WIN-X0RZAVI
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
#                                          Battery: 100% [Full]"""
# genMultiText(lines1, currRow, 1, 1)
# genTypingText("ll -p", currRow, 1, True, 1)
# lines2 = """total 204K
# drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Nov 28 12:20 frames/
# drwxr-xr-x 8 x0rzavi x0rzavi 4.0K Nov 27 11:36 .git/
# -rw-r--r-- 1 x0rzavi x0rzavi 3.1K Nov 18 15:20 .gitignore
# -rw-r--r-- 1 x0rzavi x0rzavi 106K Nov 17 12:10 gohufont-uni-14.bdf
# -rw-r--r-- 1 x0rzavi x0rzavi 1.3K Nov 17 12:10 gohufont-uni-14.pbm
# -rw-r--r-- 1 x0rzavi x0rzavi 5.1K Nov 17 12:10 gohufont-uni-14.pil
# -rw-r--r-- 1 x0rzavi x0rzavi 1.1K Nov 17 11:51 LICENSE
# -rw-r--r-- 1 x0rzavi x0rzavi  14K Nov 28 13:27 main.py
# drwxr-xr-x 3 x0rzavi x0rzavi 4.0K Nov 26 10:18 .mypy_cache/
# -rw-r--r-- 1 x0rzavi x0rzavi  26K Nov 28 12:20 output.gif
# -rw-r--r-- 1 x0rzavi x0rzavi  13K Nov 24 10:15 temp.py
# drwxr-xr-x 5 x0rzavi x0rzavi 4.0K Nov 17 12:05 venv/"""
# genMultiText(lines2, currRow, 1, 1)
#
# frame = genFrame(None)
# lines2 = ["line1", "line2"]
# lines3 = ["|line1", "|line2", "|line3"]
# lines4 = ["line1", "line2", "line3", "line4"]
# lines5 = ["line1", "line2", "line3", "line4", "line5"]
# lines10 = [
#     "|line1",
#     "|line2",
#     "|line3",
#     "|line4",
#     "|line5",
#     "|line6",
#     "|line7",
#     "|line8",
#     "|line9",
#     "|line10",
# ]
# genMultiText(lines10, 1, 1, 10)
# genMultiText(lines2, 4, 1, 10, True, True)
# genMultiText(lines3, 21, 1, 15)
# genMultiText(lines3, 3, 1, 15)

os.system(
    f"ffmpeg -hide_banner -loglevel error -r {fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif"
)  # debug
