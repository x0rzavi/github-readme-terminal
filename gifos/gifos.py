# TODO
# [x] Need blinking for multiline on next line
# [x] Not blinking if have to scroll on last line only if prompt is true; but individually working
# [] **** Appropriate number of lines to scroll with prompt
# [] Optimization + better code quality
# [] Merge genText() and genMultiText()
# [] Config file
# [] Theming
# [] Scriptable input file
# [] Remove debug statements/optional debug mode
# [] Documentation
# [] GIF maker implementation
# [] Test cases

from PIL import Image, ImageDraw, ImageFont
import random
from icecream import ic
import os  # debug

os.system("rm -fr ./frame* ./output*")  # debug

baseName = "frame_"
folderName = "./frames/"
os.mkdir(folderName)
fps = 10.0


class Terminal:
    def __init__(
        self,
        width: int,
        height: int,
        xPad: int,
        yPad: int,
        font: ImageFont.ImageFont,
        debug: bool = False,
    ) -> None:
        if debug:
            ic.configureOutput(includeContext=True)
        else:
            ic.disable()
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
        self.lineSpacing = 4
        self.numRows = (self.height - 2 * self.yPad) // (
            self.fontHeight + self.lineSpacing
        )
        self.numCols = (self.width - 2 * self.xPad) // (self.fontWidth)
        self.colInRow = {_ + 1: 1 for _ in range(self.numRows)}
        self.cursor = "_"
        self.cursorOrig = self.cursor
        self.showCursor = True
        self.prompt = "x0rzavi@github ~> "
        self.frame = self.__genFrame()

    def __alterCursor(self):
        self.cursor = self.cursorOrig if self.cursor != self.cursorOrig else " "
        ic(self.cursor)  # debug

    def toggleShowCursor(self, choice: bool = None):
        self.showCursor = not self.showCursor if choice is None else choice
        ic(self.showCursor)  # debug

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

    def __genFrame(self, frame: Image.Image = None) -> Image.Image:
        if frame is None:
            frame = Image.new("RGB", (self.width, self.height), self.bgColor)
            self.colInRow = {_ + 1: 1 for _ in range(self.numRows)}
            # frame = self.__frameDebugLines(frame)
            self.cursorToBox(1, 1)  # initialize at box (1, 1)
            return frame
        self.frameCount += 1
        fileName = baseName + str(self.frameCount) + ".png"
        frame.save(folderName + fileName, "PNG")
        ic(self.frameCount)  # debug
        return frame

    def clearFrame(self) -> None:
        self.frame = self.__genFrame()
        ic("Frame cleared")

    def cloneFrame(self, count: int = 1) -> None:
        for _ in range(count):
            self.frame = self.__genFrame(self.frame)
        ic(f"Frame cloned {count} times")

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
                f"row {rowNum} > max row {self.numRows}, using row {self.numRows} instead"
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
            ic(firstBlankRow, numBlankRows)  # debug

            if rowNum > maxRowNum:
                ic(f"{textNumLines} lines cannot be accomodated at {rowNum}")
                ic(f"Maximum possible is {maxRowNum}")
                if firstBlankRow < maxRowNum:  # needed ?????
                    ic("NEEDED!")  # debug
                    exit(1)
                    scrollTimes = textNumLines - numBlankRows
                    ic(scrollTimes)
                    self.scrollUp(scrollTimes)
                    rowNum = self.currRow
                else:
                    rowNum = maxRowNum  # enough space to print; no need to scroll

            elif firstBlankRow > rowNum:
                scrollTimes = firstBlankRow - rowNum
                ic(scrollTimes)
                self.scrollUp(scrollTimes)
        else:
            if colNum < minColNum:
                ic(f"{textNumChars} chars cannot be accomodated at column {colNum}")
                colNum = self.colInRow[rowNum]
        self.currRow, self.currCol = rowNum, colNum
        ic(self.currRow, self.currCol)  # debug

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
            ic("Not for multiline texts")  # debug
        else:
            textNumChars = len(text)
            x1, y1, _, _ = self.cursorToBox(rowNum, colNum, 1, textNumChars, contin)
            draw = ImageDraw.Draw(self.frame)
            draw.text((x1, y1), text, self.txtColor, self.font)
            self.currCol += len(text)
            self.colInRow[self.currRow] = self.currCol
            ic(self.currRow, self.currCol)  # debug

            for _ in range(count):
                if self.showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text((cx1, cy1), str(self.cursor), self.txtColor, self.font)
                self.__genFrame(self.frame)
                if self.showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
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
            ic("Both prompt and contin can't be simultaneously True")  # debug
            exit(1)

        if isinstance(text, str):
            textLines = text.splitlines()
            textNumLines = len(textLines)
        else:
            textLines = text
            textNumLines = len(text)

        if textNumLines == 1:
            ic("Not for single line texts")  # debug
        else:
            # if prompt:
            #     ic("Initialized position") # debug
            #     self.cursorToBox(rowNum, colNum, textNumLines + 2, 1, False)
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
                ic(self.currRow, self.currCol)  # debug
            self.cursorToBox(self.currRow + 1, 1, 1, 1, False)  # move down by 1 row

            if prompt:
                self.cloneFrame(1)  # wait a bit before printing new prompt
                self.genPrompt(
                    self.currRow, 1, 1
                )  # generate prompt right after printed text, i.e. 1 line below

            draw = ImageDraw.Draw(self.frame)
            for _ in range(count):
                if self.showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text((cx1, cy1), str(self.cursor), self.txtColor, self.font)
                self.__genFrame(self.frame)
                if self.showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
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
        # 0 - random - random frame count
        # 1 - fast - 1 frame count
        # 2 - medium - 2 frame count
        # 3 - slow - 3 frame count
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
            ic(self.currRow, self.currCol)

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
        ic(f"Deleted row {rowNum}")

    @staticmethod
    def genGif() -> None:
        os.system(
            f"ffmpeg -hide_banner -loglevel error -r {fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif"
        )
        ic.enable()
        ic("Generated output.gif")  # debug


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
