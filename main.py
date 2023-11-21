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
# [] Blinking cursor
# [] Prompt
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
fps = 6.0
lineSpacing = 4  # default

frameCount = 0
xPos, yPos = 0, 0
xPadding, yPadding = 15, 15
currLine = 0

font = ImageFont.load(fontFile)  # bitmap font
fontWidth, fontHeight = font.getbbox("W")[2], font.getbbox("H")[3]

numLines = (height - 2 * yPadding) // (fontHeight + lineSpacing)
# print(numLines)  # debug


def genFrame(frame: Image.Image = None, count: int = 1) -> Image.Image:
    global frameCount, linexPos
    if frame is None:
        frame = Image.new("RGB", (width, height), bgColor)
        linexPos = {_ + 1: xPadding for _ in range(numLines)}
        # return frame
    for _ in range(count):
        frameCount += 1
        fileName = baseName + str(frameCount) + ".png"
        frame.save(folderName + fileName, "PNG")
    # print("generated frame")  # debug
    return frame


def cursorToLine(lineNum: int, cont: bool = False, textNumLines: int = 1) -> bool:
    global xPos, yPos, currLine
    maxLineNum = numLines - textNumLines + 1
    if lineNum > numLines:
        print("Line {} out of bounds".format(lineNum))
        return False
    elif lineNum > maxLineNum:
        print("{} lines cannot be accomodated at line {}".format(textNumLines, lineNum))
        print("Need to print at atleast line {}".format(maxLineNum))
        return False
    else:
        if cont is False and linexPos[lineNum] != xPadding:
            scrollTimes = textNumLines
            # print(scrollTimes) # debug
            scrollUp(scrollTimes)
            xPos = xPadding
        else:
            xPos = linexPos[lineNum]
        yPos = yPadding + (lineNum - 1) * (fontHeight + lineSpacing)
        currLine = lineNum
        # print("x: {} y: {}".format(xPos, yPos))  # debug
        # print("moved cursor to line {}".format(lineNum))  # debug
        return True


def genText(text: str, lineNum: int, count: int = 1, cont: bool = False) -> None:
    global xPos, yPos, frame, currLine
    textLines = text.splitlines()
    textNumLines = len(textLines)
    if cursorToLine(lineNum, cont, textNumLines):
        for line in textLines:
            pos = (xPos, yPos)
            draw = ImageDraw.Draw(frame)
            draw.text(pos, line, txtColor, font)
            bbox = draw.textbbox(pos, line, font)
            xPos, yPos = bbox[2], bbox[3]
            yPos += lineSpacing
            linexPos[currLine] = xPos
            # print("x: {} y: {}".format(xPos, yPos))  # debug
            # draw.point((xPos, yPos), "turquoise")  # debug
            if currLine != numLines:  # no more if last line
                cursorToLine(currLine + 1, cont, 1)
        frame = genFrame(frame, count)
        # print("generated text at line {}".format(lineNum))  # debug


def genTypingText(text: str, lineNum: int, cont: bool = False, speed: int = 0) -> None:
    # speed configuration
    # 0 - random - random frames
    # 1 - fast - 1 frames
    # 2 - medium - 2 frames
    # 3 - slow - 3 frames
    if cont is False:
        cursorToLine(lineNum, cont, 1)
    if speed == 1 or speed == 2 or speed == 3:
        for char in text:
            genText(char, lineNum, speed, True)
    else:
        for char in text:
            count = random.choice([_ for _ in range(1, 4)])
            genText(char, lineNum, count, True)
    # print("generated text at line {}".format(lineNum))  # debug


def scrollUp(count: int = 1) -> None:
    global frame, linexPos, currLine
    for _ in range(count):
        croppedFrame = frame.crop((0, fontHeight + lineSpacing, width, height))
        frame = Image.new("RGB", (width, height), bgColor)
        frame.paste(croppedFrame, (0, 0))
        currLine -= 1
        keys = list(linexPos.keys())
        values = list(linexPos.values())
        shiftedValues = values[1:] + [xPadding]
        shiftedDict = dict(zip(keys, shiftedValues))
        linexPos = shiftedDict
    # print("scrolled up")  # debug


def deleteLine(lineNum: int) -> None:
    global xPos, yPos, frame, currLine
    cursorToLine(lineNum, True, 1) # continue = True; do not scroll up
    linexPos[lineNum] = xPadding
    layerImage = Image.new("RGB", (width, fontHeight + lineSpacing), bgColor)
    frame.paste(layerImage, (0, yPos))
    currLine = lineNum
    # print("x: {} y: {}".format(xPos, yPos))  # debug
    # print("deleted line {}".format(lineNum))  # debug


# TEST BED
frame = genFrame(None)  # initial blank frame
genText("Starting GifOS ", 1, 5)
genTypingText("......", 1, True)
for i in range(0x0, 0x40000000, 0x6FFFFFF):
    deleteLine(2)
    genText("Memory Check: {}".format(i), 2)
frame = genFrame(frame, 4)
deleteLine(2)
genText("Memory Check: 1048576K + 1024K Shared Memory", 2, 5)
 
frame = genFrame(None, 4)
genText("Enter username: ", 1, 5)
genTypingText("x0rzavi", 1, True)
frame = genFrame(frame, 4)
genText("Enter password: ", 2, 5)
genTypingText("***********", 2 ,True)
frame = genFrame(frame, 4)
genText("Coded by x0rzavi@github.com", numLines, 10)
 
frame = genFrame(None, 2)
genText('github-terminal-magic on main\n$> ', 1, 8)
genTypingText('fastfetch', 2, True)
multiLines1 = '''                  -`                     x0rzavi@WIN-X0RZAVI
                 .o+`                    -------------------
                `ooo/                    OS: Arch Linux x86_64
               `+oooo:                   Host: Windows Subsystem for Linux - Arch
              `+oooooo:                  Kernel: 5.15.133.1-microsoft-standard-WSL2
              -+oooooo+:                 Uptime: 12 hours, 2 mins
            `/:-:++oooo+:                Packages: 503 (pacman)
           `/++++/+++++++:               Shell: zsh 5.9
          `/++++++++++++++:              Display (westonrdp): 1920x1080 @ 60Hz
         `/+++ooooooooooooo/`            WM: WSLg (Wayland)
        ./ooosssso++osssssso+`           Terminal: tmux 3.3a
       .oossssso-````/ossssss+`          CPU: AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx (8) @ 2.10 GHz
      -osssssso.      :ssssssso.         GPU: AMD Radeon(TM) Vega 8 Graphics (1.99 GiB) [Integrated]
     :osssssss/        osssso+++.        Memory: 1.12 GiB / 6.75 GiB (17%)
    /ossssssss/        +ssssooo/-        Swap: 0 B / 2.00 GiB (0%)
  `/ossssso+/:-        -:/+osssso+-      Disk (/): 5.00 GiB / 1006.85 GiB (0%) - ext4
 `+sso+:-`                 `.-/+oso:     Disk (/mnt/c): 85.88 GiB / 200.75 GiB (43%) - 9p
`++:.                           `-/+/    Disk (/mnt/d): 224.03 GiB / 931.50 GiB (24%) - 9p
.`                                 `/    Local IP (eth0): 172.22.214.187/20 *
                                         Battery: 100% [Full]
                                         Locale: en_US.UTF-8'''
genText(multiLines1 + '\ngithub-terminal-magic on main\n$> ', 3, 15)
genTypingText('ll -p', currLine, True)
multiLines2 = '''total 176K
drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Nov 19 00:10 frames/
drwxr-xr-x 8 x0rzavi x0rzavi 4.0K Nov 18 22:22 .git/
-rw-r--r-- 1 x0rzavi x0rzavi 3.1K Nov 18 15:20 .gitignore
-rw-r--r-- 1 x0rzavi x0rzavi 106K Nov 17 12:10 gohufont-uni-14.bdf
-rw-r--r-- 1 x0rzavi x0rzavi 1.3K Nov 17 12:10 gohufont-uni-14.pbm
-rw-r--r-- 1 x0rzavi x0rzavi 5.1K Nov 17 12:10 gohufont-uni-14.pil
-rw-r--r-- 1 x0rzavi x0rzavi 1.1K Nov 17 11:51 LICENSE
-rw-r--r-- 1 x0rzavi x0rzavi 7.9K Nov 19 00:13 main.py
drwxr-xr-x 3 x0rzavi x0rzavi 4.0K Nov 18 21:35 .mypy_cache/
-rw-r--r-- 1 x0rzavi x0rzavi  20K Nov 19 00:10 output.gif
-rw-r--r-- 1 x0rzavi x0rzavi  511 Nov 18 21:01 temp.py
drwxr-xr-x 5 x0rzavi x0rzavi 4.0K Nov 17 12:05 venv/'''
genText(multiLines2, 13, 15)

os.system(
    "ffmpeg -r {fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif".format(
        fps=fps, folderName=folderName
    )
)  # debug
