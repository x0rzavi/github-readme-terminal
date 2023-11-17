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
 
def genFrame(frame: Image.Image = None, count: int = 1) -> Image.Image:
    global frameCount
    if frame is None:
        frame = Image.new("RGBA", (width, height), color=bgColor)
    for _ in range(count):
        frameCount += 1
        fileName = baseName + str(frameCount) + ".png"
        frame.save(fileName, "PNG")
    return frame

def genText(frame: Image.Image, text: str, x: int, y: int, count: int = 1) -> None:
    global xPos, yPos
    pos = (x, y)
    draw = ImageDraw.Draw(frame)
    draw.text(pos, text, txtColor, font)
    bbox = draw.textbbox(pos, text, font);
    xPos, yPos = bbox[2], bbox[3]
    yPos += lineSpacing
    draw.point((xPos, yPos), 'turquoise')
    frame = genFrame(frame, count)
    print('x: {} y: {}'.format(xPos, yPos))

frame = genFrame(None)
xPos, yPos = 15, 15

# genText(frame, 'Enter username: ', xPos, yPos)
# for char in 'x0rzavi':
#     genText(frame, char, xPos, 15)

for i in range(linesNum):
   genText(frame, 'line ' + str(i), 15, yPos)

# genText(frame, 'hello', 15, 15)
# genText(frame, 'coded', xPos, 15)
# genText(frame, 'by', xPos, 15)
# genText(frame, 'x0rzavi', 15, yPos)

# frame = genFrame(frame)
# print(frame)
# img = Image.new('RGBA', (width, height), color=bgColor)
# img.save(fileName + str(count) + '.png', 'PNG'); count += 1
# draw = ImageDraw.Draw(img)
# font = ImageFont.load(fontFile)
# fontHeight = draw.textbbox((0, 0), 'test', font=font)[3]
#
# j = 0
# for i in range(5):
#    img = Image.open(fileName + str(count - 1) + '.png')
#    draw = ImageDraw.Draw(img)
#    draw.text((15, j + fontHeight), text, fill=txtColor, font=font)
#    bbox = draw.textbbox((15, j + fontHeight), text, font=font)
#    draw.rectangle(bbox, outline='turquoise')
#    j += fontHeight + 4
#    print(bbox)
#    img.save(fileName + str(count) + '.png', 'PNG'); count += 1
