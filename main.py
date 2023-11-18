# TODO
# Prototypes
# [x] Single line printing prototype
# [x] Continuous printing prototype
# [x] Delete lines prototype
# [x] Typing prototype
# [x] Scrolling prototype
# Implementations
# [] Scrolling
# [] Delete lines
# [] Optimization + better code quality
# [] Typing simulation w/ speed
# [] Multi line printing
# [] Config file
# [] Scriptable input file
# [] Remove debug statements

import os  # debug
os.system("rm -fr frame*")  # debug

from PIL import Image, ImageDraw, ImageFont

width, height = 640, 480  # VGA
fontFile = "gohufont-uni-14.pil"
bgColor = "#181825"
txtColor = "#cdd6f4"
baseName = "frame_"
lineSpacing = 4  # default

frameCount = 0
xPos, yPos = 0, 0
xPadding, yPadding = 15, 15

font = ImageFont.load(fontFile) # bitmap font
fontWidth, fontHeight = font.getbbox("W")[2], font.getbbox("H")[3]

linesNum = (height - 2 * yPadding) // (fontHeight + lineSpacing)
linexPos = {_ + 1:xPadding for _ in range(linesNum)}
# print(linexPos) # debug

def cursorToLine(lineNum: int) -> bool:
    global xPos, yPos
    if lineNum > linesNum:
        print("Out of Bounds")
        return 0
    else:
        xPos = linexPos[lineNum]
        yPos = yPadding + (lineNum - 1) * (fontHeight + lineSpacing)
        print('moved cursor to line {}'.format(lineNum)) # debug
        return 1


def genFrame(frame: Image.Image = None, count: int = 1) -> Image.Image:
    global frameCount
    if frame is None:
        frame = Image.new("RGB", (width, height), bgColor)
        return frame
    for _ in range(count):
        frameCount += 1
        fileName = baseName + str(frameCount) + ".png"
        frame.save(fileName, "PNG")
    print('generated frame') # debug
    return frame


def genText(text: str, lineNum: int, count: int = 1) -> None:
    global xPos, yPos, frame
    if cursorToLine(lineNum):
        pos = (xPos, yPos)
        draw = ImageDraw.Draw(frame)
        draw.text(pos, text, txtColor, font)
        bbox = draw.textbbox(pos, text, font)
        xPos, yPos = bbox[2], bbox[3]
        yPos += lineSpacing
        linexPos[lineNum] = xPos
        print("x: {} y: {}".format(xPos, yPos))  # debug
        draw.point((xPos, yPos), "turquoise")  # debug
        frame = genFrame(frame, count)
    print('generated text at line {}'.format(lineNum)) # debug

def genTypingText(text: str, lineNum: int, count: int = 1) -> None:
    for char in text:
        genText(char, lineNum, count)
    print('generated text at line {}'.format(lineNum)) # debug

def scrollUp(count: int = 1) -> None:
    global frame
    for _ in range(count):
        croppedFrame = frame.crop((0, fontHeight + lineSpacing, width, height))
        frame = genFrame(None)
        frame.paste(croppedFrame, (0, 0))
        linexPos[linesNum - _] = xPadding
    print('scrolled up') # debug


def deleteLine(lineNum: int) -> None:
    global xPos, yPos, frame
    cursorToLine(lineNum)
    linexPos[lineNum] = xPadding
    layerImage = Image.new("RGB", (width, fontHeight + lineSpacing), bgColor)
    frame.paste(layerImage, (0, yPos))
    print("x: {} y: {}".format(xPos, yPos))  # debug
    print('deleted line {}'.format(lineNum)) # debug

# TEST BED
frame = genFrame(None) # initial blank frame
genText("Enter username: ", 1)
genTypingText("x0rzavi ", 1)
genText("Continued text! ", 1)

genText("Enter password: ", 2)
genTypingText("*** ", 2)

deleteLine(1)
genText("Will this work? ", 1)
genText("It worked! ", 1)

genText("Hello 24th line", 24)
genText("Hello 25th line", 25)
scrollUp(2)
genText("Hello 25th line", 25)

# os.system("ffmpeg -r 2.0 -i 'frame_%d.png' frames.gif")  # debug