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

# fontFile = "gohufont-uni-14.pil"
# font = ImageFont.load(fontFile)  # bitmap monospaced font
fontFile = "Iosevka-Regular.ttf"
font = ImageFont.truetype(fontFile, 18) # truetype monospaced font
baseName = "frame_"
folderName = "./frames/"
os.mkdir(folderName)
fps = 8.0


class Terminal:
    def __init__(
        self, width: int, height: int, xPad: int, yPad: int, font: ImageFont.ImageFont
    ) -> None:
        self.width = width
        self.height = height
        self.xPad = xPad
        self.yPad = yPad
        self.font = font
        self.bgColor = "#181825"
        self.txtColor = "#cdd6f4"
        self.frameCount = 0
        self.currRow = 0
        self.currCol = 0
        self.fontWidth = self.font.getbbox("W")[2]
        self.fontHeight = self.font.getbbox("H")[3]
        self.lineSpacing = 6
        self.numRows = (self.height - 2 * self.yPad) // (
            self.fontHeight + self.lineSpacing
        )
        self.numCols = (self.width - 2 * self.xPad) // (self.fontWidth)
        self.colInRow = {_ + 1: 1 for _ in range(self.numRows)}
        self.cursor = "_"
        self.cursorOrig = self.cursor
        self.showCursor = True
        self.frame = self.genFrame()
        self.prompt = "x0rzavi@github ~> "

    def __alterCursor(self):
        self.cursor = self.cursorOrig if self.cursor != self.cursorOrig else " "
        ic("alterCursor():", self.cursor)  # debug

    def toggleShowCursor(self, choice: bool = None):
        self.showCursor = not self.showCursor if choice is None else choice
        ic("toggleShowCursor():", self.showCursor)  # debug

    def __frameDebugLines(self, frame: Image.Image) -> Image.Image:
        # checker box to debug
        draw = ImageDraw.Draw(frame)
        for i in range(self.numRows + 1):  # (n + 1) lines
            x1 = self.xPad
            x2 = self.width - self.xPad
            y1 = y2 = self.yPad + i * (self.fontHeight + self.lineSpacing)
            draw.line([(x1, y1), (x2, y2)], "yellow")
            draw.text((0, y1), str(i + 1), "orange", self.font)  # row numbers
        for i in range(self.numCols + 1):  # (n + 1) lines
            x1 = x2 = self.xPad + i * self.fontWidth
            y1 = self.yPad
            y2 = self.height - self.yPad
            draw.line([(x1, y1), (x2, y2)], "turquoise")
        draw.line(
            [(self.xPad, self.yPad), (self.width - self.xPad, self.yPad)], "red"
        )  # top
        draw.line(
            [(self.xPad, self.yPad), (self.xPad, self.height - self.yPad)], "red"
        )  # left
        draw.line(
            [
                (self.xPad, self.height - self.yPad),
                (self.width - self.xPad, self.height - self.yPad),
            ],
            "red",
        )  # bottom
        draw.line(
            [
                (self.width - self.xPad, self.yPad),
                (self.width - self.xPad, self.height - self.yPad),
            ],
            "red",
        )  # right
        return frame

    def genFrame(self, frame: Image.Image = None) -> Image.Image:
        if frame is None:
            frame = Image.new("RGB", (self.width, self.height), self.bgColor)
            self.colInRow = {_ + 1: 1 for _ in range(self.numRows)}
            # frame = self.__frameDebugLines(frame)
            self.cursorToBox(1, 1)  # initialize at box (1, 1)
            return frame
        self.frameCount += 1
        ic("genFrame():", self.frameCount)  # debug
        fileName = baseName + str(self.frameCount) + ".png"
        frame.save(folderName + fileName, "PNG")
        return frame

    def cloneFrame(self, frame: Image.Image, count: int = 1) -> Image.Image:
        for _ in range(count):
            frame = self.genFrame(frame)
        return frame

    def cursorToBox(
        self,
        rowNum: int,
        colNum: int,
        textNumLines: int = 1,
        textNumChars: int = 1,
        contin: bool = False,
    ) -> tuple:
        if rowNum < 1 or colNum < 1 or colNum > self.numCols:
            raise ValueError
        elif rowNum > self.numRows:
            ic(
                "cursorToBox():",
                "rowNum exceeds max row number, using",
                self.numRows,
                "instead",
            )
            rowNum = self.numRows
        maxRowNum = self.numRows - textNumLines + 1  # maximum row that can be permitted
        minColNum = self.colInRow[rowNum]

        if contin is False:
            numBlankRows = 0
            firstBlankRow = self.numRows + 1  # all rows are filled
            for i in range(self.numRows, rowNum - 1, -1):
                if self.colInRow[i] == 1:
                    firstBlankRow = i
                    numBlankRows += 1
                else:
                    break
            ic("cursorToBox():", firstBlankRow, numBlankRows)

            if rowNum > maxRowNum:
                ic("cursorToBox():", textNumLines, "cannot be accomodated at", rowNum)
                ic("cursorToBox():", "maximum possible", maxRowNum)
                if firstBlankRow < maxRowNum:  # needed ?????
                    ic("NEEDED!")  # debug
                    exit(1)
                    scrollTimes = textNumLines - numBlankRows
                    ic("cursorToBox():", scrollTimes)
                    self.scrollUp(scrollTimes)
                    rowNum = self.currRow
                else:
                    rowNum = maxRowNum  # enough space to print; no need to scroll

            elif firstBlankRow > rowNum:
                scrollTimes = firstBlankRow - rowNum
                ic("cursorToBox():", scrollTimes)
                self.scrollUp(scrollTimes)
        else:
            if colNum < minColNum:
                ic(
                    "cursorToBox():",
                    textNumChars,
                    "cannot be accomodated at",
                    colNum,
                )
                colNum = self.colInRow[rowNum]
        self.currRow, self.currCol = rowNum, colNum
        ic("cursorToBox():", self.currRow, self.currCol)  # debug

        x1 = self.xPad + (colNum - 1) * self.fontWidth
        y1 = self.yPad + (rowNum - 1) * (self.fontHeight + self.lineSpacing)
        x2 = self.xPad + colNum * self.fontWidth
        y2 = self.yPad + rowNum * (self.fontHeight + self.lineSpacing)
        return x1, y1, x2, y2

    def genText(
        self, text: str, rowNum: int, colNum: int, count: int = 1, contin: bool = False
    ) -> None:
        textNumLines = len(text.splitlines())
        if textNumLines > 1:
            ic("genText():", "Not for multiline texts")  # debug
        else:
            textNumChars = len(text)
            x1, y1, _, _ = self.cursorToBox(rowNum, colNum, 1, textNumChars, contin)
            draw = ImageDraw.Draw(self.frame)
            draw.text((x1, y1), text, self.txtColor, self.font)
            self.currCol += len(text)
            self.colInRow[self.currRow] = self.currCol
            ic("genText():", self.currRow, self.currCol)  # debug

            for _ in range(count):
                if self.showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text((cx1, cy1), str(self.cursor), self.txtColor, self.font)
                self.genFrame(self.frame)
                if self.showCursor:
                    blankBoxImage = Image.new(
                        "RGB",
                        (self.fontWidth, self.fontHeight + self.lineSpacing),
                        self.bgColor,
                    )
                    self.frame.paste(blankBoxImage, (cx1, cy1))
                    self.__alterCursor()

    def genMultiText(
        self,
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

        # global frame, currRow, currCol, colInRow

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
                x1, y1, _, _ = self.cursorToBox(
                    rowNum + i, colNum, 1, textNumChars, contin
                )
                draw = ImageDraw.Draw(self.frame)
                draw.text((x1, y1), line, self.txtColor, self.font)
                self.currCol += len(line)
                self.colInRow[self.currRow] = self.currCol
                ic("genMultiText():", self.currRow, self.currCol)  # debug

            if prompt:
                self.cloneFrame(self.frame, 1)  # wait a bit before printing new prompt
                self.genPrompt(self.currRow + 1, 1, 1)  # next to currRow

            for _ in range(count):
                if self.showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text((cx1, cy1), str(self.cursor), self.txtColor, self.font)
                self.genFrame(self.frame)
                if self.showCursor:
                    blankBoxImage = Image.new(
                        "RGB",
                        (self.fontWidth, self.fontHeight + self.lineSpacing),
                        self.bgColor,
                    )
                    self.frame.paste(blankBoxImage, (cx1, cy1))
                    self.__alterCursor()

    def genPrompt(self, rowNum: int, colNum: int, count: int = 1):
        origCursorState = self.showCursor
        self.toggleShowCursor(True)
        self.genText(self.prompt, rowNum, colNum, count, False)
        self.showCursor = origCursorState

    def genTypingText(
        self, text: str, rowNum: int, colNum: int, contin: bool = False, speed: int = 0
    ) -> None:
        # speed configuration
        # 0 - random - random frames
        # 1 - fast - 1 frames
        # 2 - medium - 2 frames
        # 3 - slow - 3 frames
        if contin is False:
            self.cursorToBox(rowNum, colNum, 1, 1, contin)
        if speed == 1 or speed == 2 or speed == 3:
            for char in text:
                self.genText(char, rowNum, self.colInRow[rowNum], speed, True)
        else:
            for char in text:
                count = random.choice([1, 2, 3])
                self.genText(char, rowNum, self.colInRow[rowNum], count, True)

    def scrollUp(self, count: int = 1) -> None:
        for _ in range(count):
            croppedFrame = self.frame.crop(
                (0, self.fontHeight + self.lineSpacing, self.width, self.height)
            )  # make room for 1 extra line (fontHeight + lineSpacing)
            self.frame = Image.new("RGB", (self.width, self.height), self.bgColor)
            self.frame.paste(croppedFrame, (0, 0))
            self.currRow -= 1  # move cursor to where it was

            keys = list(self.colInRow.keys())
            values = list(self.colInRow.values())
            shiftedValues = values[1:] + [1]
            shiftedDict = dict(zip(keys, shiftedValues))
            self.colInRow = shiftedDict
            ic("scrollUp():", self.currRow, self.currCol)

    def deleteRow(self, rowNum: int) -> None:
        _, y1, _, _ = self.cursorToBox(
            rowNum, 1, 1, 1, True
        )  # continue = True; do not scroll up
        self.colInRow[rowNum] = 1
        blankLineImage = Image.new(
            "RGB",
            (self.width - self.xPad, self.fontHeight + self.lineSpacing),
            self.bgColor,
        )
        self.frame.paste(blankLineImage, (0, y1))


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


## TEST BED
t = Terminal(640, 480, 15, 15, font)
t.toggleShowCursor(False)
t.genText("", 1, 1, 5, False)
t.genText("Starting GIF OS ", 1, 1, 5, False)
t.genTypingText(".....", 1, 1, True)
for i in range(0x0, 0x40000000, 0x7FFFFFF):
    if i < 0x20000000:
        t.cloneFrame(t.frame, 2)
    t.deleteRow(2)
    t.genText(f"Memory Check: {i}", 2, 1)
t.cloneFrame(t.frame, 5)
t.deleteRow(2)
t.genText("Memory Check: 1048576KB OK", 2, 1, 5)

t.frame = t.genFrame()
t.toggleShowCursor(True)
t.genText("", 1, 1, 5)
t.toggleShowCursor(False)
t.genText("Enter username: ", 1, 1, 5)
t.toggleShowCursor(True)
t.genTypingText("x0rzavi", 1, 1, True)
t.cloneFrame(t.frame, 5)
t.toggleShowCursor(True)
t.genText("", 2, 1, 5)
t.toggleShowCursor(False)
t.genText("Enter password: ", 2, 1, 5)
t.toggleShowCursor(True)
t.genTypingText("*********", 2, 1, True)
t.genText("", 3, 1, 5)
t.genText("Coded by x0rzavi :D", t.numRows, 1, 10)
t.cloneFrame(t.frame, 2)

t.frame = t.genFrame()
t.toggleShowCursor(True)
t.genPrompt(1, 1, 1)
t.genTypingText("fetch", 1, 1, True, 1)
t.genText("", t.currRow + 1, 1, 1)
lines1 = r"""        /\        x0rzavi@WIN-X0RZAVI
       /  \
      /\   \      OS: Arch Linux x86_64
     /      \     Kernel: Linux 5.15.133.1-microsoft-standard-WSL2
    /   ,,   \    Uptime: 2 hours, 42 minutes
   /   |  |  -\   Packages: 494 (pacman)
  /_-''    ''-_\  Shell: zsh 5.9
                  CPU: AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx (8) @ 2.096MHz
                  Memory: 548MB / 7073MB
"""
t.genMultiText(lines1, t.currRow, 1, 10)
t.genTypingText("ll -p", t.currRow, 1, True, 1)
lines2 = r"""total 180K
drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Dec  3 15:05 frames/
drwxr-xr-x 8 x0rzavi x0rzavi 4.0K Dec  3 10:48 .git/
-rw-r--r-- 1 x0rzavi x0rzavi 3.1K Dec  1 11:16 .gitignore
-rw-r--r-- 1 x0rzavi x0rzavi 106K Nov 17 12:10 gohufont-uni-14.bdf
-rw-r--r-- 1 x0rzavi x0rzavi 1.3K Nov 17 12:10 gohufont-uni-14.pbm
-rw-r--r-- 1 x0rzavi x0rzavi 5.1K Nov 17 12:10 gohufont-uni-14.pil
-rw-r--r-- 1 x0rzavi x0rzavi 1.1K Nov 17 11:51 LICENSE
-rw-r--r-- 1 x0rzavi x0rzavi  16K Dec  3 15:05 main.py
drwxr-xr-x 3 x0rzavi x0rzavi 4.0K Dec  3 15:04 .mypy_cache/
-rw-r--r-- 1 x0rzavi x0rzavi  13K Nov 24 10:15 temp.py
drwxr-xr-x 5 x0rzavi x0rzavi 4.0K Nov 17 12:05 venv/
drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Dec  1 10:24 .vscode/"""
t.genMultiText(lines2, t.currRow, 1, 10)

# t = Terminal(640, 480, 15, 15, font)
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
# t.genMultiText(lines10, 1, 1, 1)
# t.genMultiText(lines2, 4, 1, 1, False)
# t.genMultiText(lines3, 21, 1, 1, False)
# t.genMultiText(lines3, 3, 1, 1, False)


os.system(
    f"ffmpeg -hide_banner -loglevel error -r {fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif"
)  # debug
