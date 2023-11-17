# TODO
# [x] Scrolling prototype
# [] Optimization + better implementation
# [] Typing simulation w/ speed
# [] Single line printing
# [] Multi line printing
# [] Config file
# [] Scriptable input file

from PIL import Image, ImageDraw, ImageFont

width, height = 640, 480  # VGA
fontFile = "gohufont-uni-14.pil"
bgColor = "#181825"
txtColor = "#cdd6f4"
baseName = "frame_"
frameCount = 0
xPos, yPos = 0, 0
xPadding, yPadding = 15, 15
lineSpacing = 4

font = ImageFont.load(fontFile)
fontHeight = font.getbbox('')[3]

def linesNumCalc(height: int, yPadding: int, fontHeight: int, lineSpacing: int) -> int:
    linesNum = (height - 2 * yPadding) // (fontHeight + lineSpacing)
    return linesNum

linesNum = linesNumCalc(height, yPadding, fontHeight, lineSpacing)
print(linesNum)
 
def cursorToLine(lineNum: int) -> None:
    global xPos, yPos
    if lineNum > linesNum:
        return 0
    else:
        xPos = xPadding
        yPos = yPadding + (lineNum - 1) * (fontHeight + lineSpacing)
        return 1

def genFrame(frame: Image.Image = None, count: int = 1) -> Image.Image:
    global frameCount
    if frame is None:
        frame = Image.new("RGBA", (width, height), bgColor)
    for _ in range(count):
        frameCount += 1
        fileName = baseName + str(frameCount) + ".png"
        frame.save(fileName, "PNG")
    return frame

def genText(frame: Image.Image, text: str, lineNum: int, count: int = 1) -> None:
    global xPos, yPos
    if cursorToLine(lineNum):
        pos = (xPos, yPos)
        draw = ImageDraw.Draw(frame)
        draw.text(pos, text, txtColor, font)
        bbox = draw.textbbox(pos, text, font);
        xPos, yPos = bbox[2], bbox[3]
        yPos += lineSpacing
        frame = genFrame(frame, count)

        # debug
        draw.point((xPos, yPos), 'turquoise')
        print('x: {} y: {}'.format(xPos, yPos))
    else:
        print('Out of Bounds')

def scrollUp(frame: Image.Image) -> Image.Image:
    croppedFrame = frame.crop((0, fontHeight + lineSpacing, width, height))
    frame = Image.new("RGBA", (width, height), bgColor)
    frame.paste(croppedFrame, (0, 0))
    return frame
    
frame = genFrame(None)
genText(frame, 'Hello first line', 1)
genText(frame, 'Hello second line', 2)
genText(frame, 'Hello second last line', 24)
genText(frame, 'Hello last line', 25)

# croppedImage = frame.crop((0, fontHeight + lineSpacing, width, height))
# croppedImage.save('frame_cropped.png')
# newImage = Image.new("RGBA", (width, height), bgColor)
# newImage.paste(croppedImage, (0, 0))
# newImage.save('frame_final.png')

frame = scrollUp(frame)
genText(frame, 'Hello again last line', 25)
frame = scrollUp(frame)
genText(frame, 'Hello again last line', 25)
frame = scrollUp(frame)
genText(frame, 'Hello again last line', 25)

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