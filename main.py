# TODO
# Prototypes
# [x] Single line printing prototype
# [x] Multi line printing prototype
# [x] Continuous printing prototype
# [x] Delete lines prototype
# [x] Typing prototype
# [x] Scrolling prototype
# Implementations
# [x] Delete lines
# [x] Typing simulation w/ speed
# [x] Scrolling
# [] Optimization + better code quality
# [] Config file
# [] Theming
# [] Scriptable input file
# [] Remove debug statements
# [] GIF maker implementation

import os  # debug

os.system("rm -fr frame* output*")  # debug

from PIL import Image, ImageDraw, ImageFont
import random

width, height = 640, 480  # VGA
fontFile = "gohufont-uni-14.pil"
bgColor = "#181825"
txtColor = "#cdd6f4"
baseName = "frame_"
folderName = "./frames/"
os.mkdir(folderName)
fps = 10.0
lineSpacing = 4  # default

frameCount = 0
xPos, yPos = 0, 0
xPadding, yPadding = 15, 15
currLine = 0

font = ImageFont.load(fontFile)  # bitmap font
fontWidth, fontHeight = font.getbbox("W")[2], font.getbbox("H")[3]

linesNum = (height - 2 * yPadding) // (fontHeight + lineSpacing)
# print(linesNum)  # debug
linexPos = {_ + 1: xPadding for _ in range(linesNum)}


def genFrame(frame: Image.Image = None, count: int = 1) -> Image.Image:
    global frameCount, linexPos
    if frame is None:
        frame = Image.new("RGB", (width, height), bgColor)
        return frame
    for _ in range(count):
        frameCount += 1
        fileName = baseName + str(frameCount) + ".png"
        frame.save(folderName + fileName, "PNG")
    print("generated frame")  # debug
    return frame


def cursorToLine(lineNum: int) -> int:
    global xPos, yPos, currLine
    if lineNum > linesNum:
        print("Out of Bounds", currLine)
        return 0
    else:
        xPos = linexPos[lineNum]
        yPos = yPadding + (lineNum - 1) * (fontHeight + lineSpacing)
        currLine = lineNum
        print("x: {} y: {}".format(xPos, yPos))  # debug
        print("moved cursor to line {}".format(lineNum))  # debug
        return 1


def scrollUp(count: int = 1) -> None:
    global frame, linexPos, currLine
    for _ in range(count):
        croppedFrame = frame.crop((0, fontHeight + lineSpacing, width, height))
        frame = genFrame(None)
        frame.paste(croppedFrame, (0, 0))
        currLine -= 1
        keys = list(linexPos.keys())
        values = list(linexPos.values())
        shiftedValues = values[1:] + [xPadding]
        shiftedDict = dict(zip(keys, shiftedValues))
        linexPos = shiftedDict
    print("scrolled up")  # debug


def genText(text: str, lineNum: int, count: int = 1) -> None:
    global xPos, yPos, frame, currLine
    if cursorToLine(lineNum):
        textLines = text.splitlines()
        textLinesNum = len(textLines)
        linesDiff = linesNum - lineNum
        if textLinesNum > linesDiff: # no more space at bottom
            scrollTimes = textLinesNum - linesDiff
            scrollUp(scrollTimes)
            cursorToLine(lineNum - scrollTimes + 1)
        else:
            cursorToLine(lineNum)
        for line in textLines:
            pos = (xPos, yPos)
            draw = ImageDraw.Draw(frame)
            draw.text(pos, line, txtColor, font)
            bbox = draw.textbbox(pos, line, font)
            xPos, yPos = bbox[2], bbox[3]
            yPos += lineSpacing
            linexPos[currLine] = xPos
            print("x: {} y: {}".format(xPos, yPos))  # debug
            draw.point((xPos, yPos), "turquoise")  # debug
            if currLine != linesNum: # no more if last line
                cursorToLine(currLine + 1)

    frame = genFrame(frame, count)
    print("generated text at line {}".format(lineNum))  # debug


def genTypingText(text: str, lineNum: int, speed: int = 0) -> None:
    # speed configuration
    # 0 - random - random frames
    # 1 - fast - 1 frames
    # 2 - medium - 2 frames
    # 3 - slow - 3 frames
    if speed == 1 or speed == 2 or speed == 3:
        for char in text:
            genText(char, lineNum, speed)
    else:
        for char in text:
            count = random.choice([_ for _ in range(1, 4)])
            genText(char, lineNum, count)
    print("generated text at line {}".format(lineNum))  # debug


def deleteLine(lineNum: int) -> None:
    global xPos, yPos, frame
    cursorToLine(lineNum)
    linexPos[lineNum] = xPadding
    layerImage = Image.new("RGB", (width, fontHeight + lineSpacing), bgColor)
    frame.paste(layerImage, (0, yPos))
    print("x: {} y: {}".format(xPos, yPos))  # debug
    print("deleted line {}".format(lineNum))  # debug


# TEST BED
frame = genFrame(None)  # initial blank frame
# genText("Starting GifOS", 1, 5)
# genTypingText("...", 1, 2)
# for i in range(0x0, 0x40000000, 0x6FFFFFF):
#     deleteLine(2)
#     genText("Memory Check: {}".format(i), 2, 1)
# frame = genFrame(frame, 4)
# deleteLine(2)
# genText("Memory Check: 1048576K + 1024K Shared Memory", 2, 5)
#
# frame = genFrame(None)
# frame = genFrame(frame, 4)
# genText("Enter username: ", 1, 5)
# genTypingText("x0rzavi", 1)
# genFrame(frame, 3)
# genText("Enter password: ", 2, 5)
# genTypingText("*******", 2, 3)
# genFrame(frame, 3)
# genTypingText("Coded by x0rzavi@github.com", linesNum, 10)
multiLines = """Hello
my
name
is
Avishek Sen
This is a multiline
text sample
with scrolling"""
genText(multiLines, 20)
genText(multiLines, 1)
genText(multiLines, 8)
genText("hello 25", 25)
# genText("hello 22", 22)
# genText("hello 24", 24)
# genText("hello 25", 25)
# print(linexPos)
# genText("hi", 24)
# print(linexPos)

# os.system(
#     "ffmpeg -r {fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif".format(fps=fps, folderName=folderName)
# )  # debug
