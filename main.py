# TODO
# [x] Scrolling prototype
# [] Scrolling
# [x] Delete lines prototype
# [] Delete lines
# [] Optimization + better implementation
# [x] Typing prototype
# [] Typing simulation w/ speed
# [] Single line printing
# [] Multi line printing
# [] Config file
# [] Scriptable input file

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


def cursorToLine(lineNum: int) -> int:
    global xPos, yPos
    if lineNum > linesNum:
        print("Out of Bounds")
        return 0
    else:
        xPos = xPadding
        yPos = yPadding + (lineNum - 1) * (fontHeight + lineSpacing)
        return 1


def genFrame(frame: Image.Image = None, count: int = 1) -> Image.Image:
    global frameCount
    if frame is None:
        frame = Image.new("RGBA", (width, height), bgColor)
        return frame
    for _ in range(count):
        frameCount += 1
        fileName = baseName + str(frameCount) + ".png"
        frame.save(fileName, "PNG")
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
        print("x: {} y: {}".format(xPos, yPos))  # debug
        draw.point((xPos, yPos), "turquoise")  # debug
        frame = genFrame(frame, count)


def scrollUp(count: int = 1) -> None:
    global frame
    for _ in range(count):
        croppedFrame = frame.crop((0, fontHeight + lineSpacing, width, height))
        frame = genFrame(None)
        frame.paste(croppedFrame, (0, 0))


def deleteLine(lineNum: int) -> None:
    global xPos, yPos, frame
    cursorToLine(lineNum)
    layerImage = Image.new("RGBA", (width, fontHeight + lineSpacing), bgColor)
    frame.paste(layerImage, (xPos, yPos))

def genTypingText(text: str, lineNum: int, count: int = 1) -> None:
    global xPos, yPos, frame
    if cursorToLine(lineNum):
        draw = ImageDraw.Draw(frame)
        yPosConst = yPos
        for char in text:
            yPos = yPosConst
            draw.text((xPos, yPos), char, txtColor, font)
            bbox = draw.textbbox((xPos, yPos), char, font)
            xPos, yPos = bbox[2], bbox[3]
            print("x: {} y: {}".format(xPos, yPos))  # debug
            draw.point((xPos, yPos), "turquoise")  # debug
            frame = genFrame(frame, count)


frame = genFrame(None) # initial blank frame
# genText("_", 1, 5)
# deleteLine(1)
genTypingText("Hello", 1)
genText("Hello", 2)
# genText("Hello 1st line", 1)
# genText("Hello 13th line", 13)
# genText("Hello 14th line", 14)
# deleteLine(13)
# genText('Hello 25th line', 25)
# genText('Hello 27th line', 27)

# scrollUp()
# genText("Hello 25th line", 25)
# scrollUp()
# genText("Hello 25th line", 25)

# Typing Prototype
# genText(frame, 'Enter username: ', xPos, yPos)
# for char in 'x0rzavi':
#     genText(frame, char, xPos, 15)
# for i in range(linesNum):
#    genText(frame, 'line ' + str(i), 15, yPos)

# genText(frame, 'hello', 15, 15)
# genText(frame, 'coded', xPos, 15)
# genText(frame, 'by', xPos, 15)
# genText(frame, 'x0rzavi', 15, yPos)
