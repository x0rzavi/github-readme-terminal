# TODO
# [x] Handle dynamic font size
# [] Configure prompt option
# [] Support all ANSI escape sequence forms
# [] Hardcode highlighted prompt
# [] Optimization + better code quality
# [] Merge genText() + genMultiText() + genRichText()
# [] Config file
# [] Theming
# [] Scriptable input file
# [] Documentation
# [] GIF maker implementation
# [] Test cases

import os  # debug
import re
import random
from icecream import ic
from PIL import Image, ImageDraw, ImageFont
from .utils.convertAnsiEscape import convertAnsiEscape

os.system("rm -fr ./frame* ./output*")  # debug

baseName = "frame_"
folderName = "./frames/"
os.mkdir(folderName)


class Terminal:
    def __init__(
        self,
        width: int,
        height: int,
        xPad: int,
        yPad: int,
        fontFile: str,
        fontSize: int = 16,
        debug: bool = False,
    ) -> None:
        ic.configureOutput(includeContext=True)
        if not debug:
            ic.disable()
        self.__width = width
        self.__height = height
        self.__xPad = xPad
        self.__yPad = yPad
        self.__bgColor = self.__prevBgColor = "#101415"
        self.__txtColor = "#F2F4F5"
        self.__frameCount = 0
        self.currRow = 0
        self.currCol = 0
        self.__fontFile = fontFile
        self.__fontSize = fontSize
        self.setFont(self.__fontFile, self.__fontSize)
        self.__cursor = "_"
        self.__cursorOrig = self.__cursor
        self.__showCursor = True
        self.__blinkCursor = True
        self.__fps = 20.0
        self.prompt = "x0rzavi@github ~> "
        self.__frame = self.__genFrame()

    def setTxtColor(self, txtColor: str = "#F2F4F5") -> None:  # rework later
        self.__txtColor = txtColor

    def setBgColor(self, bgColor: str = "#101415") -> None:  # rework later
        self.__prevBgColor = self.__bgColor
        self.__bgColor = bgColor

    def toggleHighlight(self) -> None:  # rework later
        self.setTxtColor(
            "#7FC8D8"
        ) if self.__txtColor == "#F2F4F5" else self.setTxtColor("#F2F4F5")

    def __checkFontType(
        self, fontFile: str, fontSize: int
    ) -> ImageFont.ImageFont | ImageFont.FreeTypeFont | None:
        try:
            font = ImageFont.truetype(fontFile, fontSize)
            return font
        except OSError:
            pass

        try:
            print(f"INFO: {fontFile} is BitMap. Ignoring size {fontSize}")
            font = ImageFont.load(fontFile)
            return font
        except OSError:
            print(f"ERROR: unknown font {fontFile}")
            return None

    def setFont(self, fontFile: str, fontSize: int = 16) -> None:
        self.__font = self.__checkFontType(fontFile, fontSize)
        if self.__font:
            self.__lineSpacing = 4
            if self.__checkMonospaceFont(self.__font)["check"]:
                self.__fontWidth = self.__font.getbbox("W")[
                    2
                ]  # empirically widest character
            else:
                self.__fontWidth = self.__checkMonospaceFont(self.__font)["avgWidth"]
            self.__fontHeight = self.__font.getbbox(r"|(/QMW")[
                3
            ]  # empirically tallest characters
            self.numRows = (self.__height - 2 * self.__yPad) // (
                self.__fontHeight + self.__lineSpacing
            )
            self.numCols = (self.__width - 2 * self.__xPad) // (self.__fontWidth)
            self.__colInRow = {_ + 1: 1 for _ in range(self.numRows)}
            # self.clearFrame()
            ic(self.__font)  # debug

    def setFps(self, fps: float) -> None:
        self.__fps = fps

    def toggleShowCursor(self, choice: bool = None) -> None:
        self.__showCursor = not self.__showCursor if choice is None else choice
        ic(self.__showCursor)  # debug

    def toggleBlinkCursor(self, choice: bool = None) -> None:
        self.__blinkCursor = not self.__blinkCursor if choice is None else choice
        ic(self.__blinkCursor)  # debug

    def __checkMonospaceFont(
        self, font: ImageFont.ImageFont | ImageFont.FreeTypeFont
    ) -> dict:
        widths = [font.getbbox(chr(i))[2] for i in range(ord("A"), ord("Z") + 1)]
        avgWidth = int(round(sum(widths) / len(widths), 0))
        return {"check": max(widths) == min(widths), "avgWidth": avgWidth}

    def __alterCursor(self) -> None:
        self.__cursor = self.__cursorOrig if self.__cursor != self.__cursorOrig else " "
        ic(self.__cursor)  # debug

    def __frameDebugLines(self, frame: Image.Image) -> Image.Image:
        # checker box to debug
        draw = ImageDraw.Draw(frame)
        for i in range(self.numRows + 1):  # (n + 1) lines
            x1 = self.__xPad
            x2 = self.__width - self.__xPad
            y1 = y2 = self.__yPad + i * (self.__fontHeight + self.__lineSpacing)
            draw.line([(x1, y1), (x2, y2)], "yellow")
            draw.text((0, y1), str(i + 1), "orange", self.__font)  # row numbers
        for i in range(self.numCols + 1):  # (n + 1) lines
            x1 = x2 = self.__xPad + i * self.__fontWidth
            y1 = self.__yPad
            y2 = self.__height - self.__yPad
            draw.line([(x1, y1), (x2, y2)], "turquoise")
        draw.line(
            [(self.__xPad, self.__yPad), (self.__width - self.__xPad, self.__yPad)],
            "red",
        )  # top
        draw.line(
            [(self.__xPad, self.__yPad), (self.__xPad, self.__height - self.__yPad)],
            "red",
        )  # left
        draw.line(
            [
                (self.__xPad, self.__height - self.__yPad),
                (self.__width - self.__xPad, self.__height - self.__yPad),
            ],
            "red",
        )  # bottom
        draw.line(
            [
                (self.__width - self.__xPad, self.__yPad),
                (self.__width - self.__xPad, self.__height - self.__yPad),
            ],
            "red",
        )  # right
        return frame

    def __genFrame(self, frame: Image.Image = None) -> Image.Image:
        if frame is None:
            frame = Image.new("RGB", (self.__width, self.__height), self.__bgColor)
            self.__colInRow = {_ + 1: 1 for _ in range(self.numRows)}
            # frame = self.__frameDebugLines(frame)
            self.cursorToBox(1, 1)  # initialize at box (1, 1)
            return frame
        self.__frameCount += 1
        fileName = baseName + str(self.__frameCount) + ".png"
        frame.save(folderName + fileName, "PNG")
        print(f"INFO: Generated frame #{self.__frameCount}")  # debug
        return frame

    def clearFrame(self) -> None:
        self.__frame = self.__genFrame()
        ic("Frame cleared")

    def cloneFrame(self, count: int = 1) -> None:
        for _ in range(count):
            self.__frame = self.__genFrame(self.__frame)
        ic(f"Frame cloned {count} times")

    def cursorToBox(
        self,
        rowNum: int,
        colNum: int,
        textNumLines: int = 1,
        textNumChars: int = 1,
        contin: bool = False,
    ) -> tuple:
        if rowNum < 1 or colNum < 1:  # dont care about exceeding colNum
            raise ValueError
        elif rowNum > self.numRows:
            ic(
                f"row {rowNum} > max row {self.numRows}, using row {self.numRows} instead"
            )
            rowNum = self.numRows
        maxRowNum = self.numRows - textNumLines + 1  # maximum row that can be permitted
        minColNum = self.__colInRow[rowNum]

        if contin is False:
            numBlankRows = 0
            firstBlankRow = self.numRows + 1  # all rows are filled
            for i in range(self.numRows, rowNum - 1, -1):
                if self.__colInRow[i] == 1:
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
                colNum = self.__colInRow[rowNum]
        self.currRow, self.currCol = rowNum, colNum
        ic(self.currRow, self.currCol)  # debug

        x1 = self.__xPad + (colNum - 1) * self.__fontWidth
        y1 = self.__yPad + (rowNum - 1) * (self.__fontHeight + self.__lineSpacing)
        x2 = self.__xPad + colNum * self.__fontWidth
        y2 = self.__yPad + rowNum * (self.__fontHeight + self.__lineSpacing)
        return x1, y1, x2, y2

    def genText(
        self,
        text: str,
        rowNum: int,
        colNum: int = 1,
        count: int = 1,
        contin: bool = False,
    ) -> None:
        textNumLines = len(text.splitlines())
        if textNumLines > 1:
            ic("Not for multiline texts")  # debug
        else:
            textNumChars = len(text)
            x1, y1, _, _ = self.cursorToBox(rowNum, colNum, 1, textNumChars, contin)
            draw = ImageDraw.Draw(self.__frame)
            draw.text((x1, y1), text, self.__txtColor, self.__font)
            self.currCol += len(text)
            self.__colInRow[self.currRow] = self.currCol
            ic(self.currRow, self.currCol)  # debug

            for _ in range(count):
                if self.__showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text(
                        (cx1, cy1), str(self.__cursor), self.__txtColor, self.__font
                    )
                self.__genFrame(self.__frame)
                if self.__showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    blankBoxImage = Image.new(
                        "RGB",
                        (self.__fontWidth, self.__fontHeight + self.__lineSpacing),
                        self.__bgColor,
                    )
                    self.__frame.paste(blankBoxImage, (cx1, cy1))
                    if (
                        self.__blinkCursor
                        and self.__frameCount % (self.__fps // 3) == 0
                    ):  # alter cursor such that blinks every one-third second
                        self.__alterCursor()

    def genMultiText(
        self,
        text: str | list,
        rowNum: int,
        colNum: int = 1,
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
                draw = ImageDraw.Draw(self.__frame)
                draw.text((x1, y1), line, self.__txtColor, self.__font)
                self.currCol += len(line)
                self.__colInRow[self.currRow] = self.currCol
                ic(self.currRow, self.currCol)  # debug
            self.cursorToBox(self.currRow + 1, 1, 1, 1, False)  # move down by 1 row

            if prompt:
                self.cloneFrame(1)  # wait a bit before printing new prompt
                self.genPrompt(
                    self.currRow, 1, 1
                )  # generate prompt right after printed text, i.e. 1 line below

            draw = ImageDraw.Draw(self.__frame)
            for _ in range(count):
                if self.__showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text(
                        (cx1, cy1), str(self.__cursor), self.__txtColor, self.__font
                    )
                self.__genFrame(self.__frame)
                if self.__showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    blankBoxImage = Image.new(
                        "RGB",
                        (self.__fontWidth, self.__fontHeight + self.__lineSpacing),
                        self.__bgColor,
                    )
                    self.__frame.paste(blankBoxImage, (cx1, cy1))
                    if (
                        self.__blinkCursor
                        and self.__frameCount % (self.__fps // 3) == 0
                    ):  # alter cursor such that blinks every one-third second
                        self.__alterCursor()

    def genTypingText(
        self,
        text: str,
        rowNum: int,
        colNum: int = 1,
        contin: bool = False,
        speed: int = 0,
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
                self.genText(char, rowNum, self.__colInRow[rowNum], speed, True)
        else:
            for char in text:
                count = random.choice([1, 2, 3])
                self.genText(char, rowNum, self.__colInRow[rowNum], count, True)

    def genRichText(
        self,
        text: str | list,
        rowNum: int,
        colNum: int = 1,
        count: int = 1,
        # prompt: bool = True,
        contin: bool = False,
    ) -> None:
        # if prompt and contin:
        #     ic("Both prompt and contin can't be simultaneously True")  # debug
        #     exit(1)

        if isinstance(text, str):
            textLines = text.splitlines()
            textNumLines = len(textLines)
        else:
            textLines = text
            textNumLines = len(text)

        if textNumLines == 1:
            ic("Not for single line texts")  # debug
        else:
            self.cursorToBox(
                rowNum, colNum, textNumLines, 1, contin
            )  # initialize position
            pattern = r"(\\x1b\[[0-?]*[ -/]*[@-~]|\x1b\[[0-?]*[ -/]*[@-~])"
            for i in range(textNumLines):
                line = textLines[i]
                words = [word for word in re.split(pattern, line) if word]
                for word in words:
                    if word.startswith(("\x1b[", "\\x1b[")):
                        codes = (
                            word.lstrip("\x1b[").lstrip("\\x1b[").rstrip("m").split(";")
                        )
                        for code in codes:
                            if code == "0":  # reset with default
                                self.setTxtColor()
                                self.setBgColor()
                                continue
                            else:
                                codeInfo = convertAnsiEscape.convert(code)
                                if codeInfo:
                                    if codeInfo.op == "txtColor":
                                        self.setTxtColor(codeInfo.data)
                                        continue
                                    if codeInfo.op == "bgColor":
                                        self.setBgColor(codeInfo.data)
                                        continue
                    else:
                        textNumChars = len(word)
                        x1, y1, _, _ = self.cursorToBox(
                            rowNum + i, colNum, 1, textNumChars, True
                        )
                        draw = ImageDraw.Draw(self.__frame)
                        if (
                            self.__prevBgColor != self.__bgColor
                        ):  # reduce unnecessary operations
                            rx1, ry1, rx2, ry2 = draw.textbbox(
                                (x1, y1), word, self.__font
                            )  # change bgColor
                            draw.rectangle((rx1, ry1, rx2, ry2), self.__bgColor)
                        draw.text((x1, y1), word, self.__txtColor, self.__font)
                        self.currCol += len(word)
                        self.__colInRow[self.currRow] = self.currCol
                        ic(self.currRow, self.currCol)  # debug
            self.cursorToBox(self.currRow + 1, 1, 1, 1, False)  # move down by 1 row

            # if prompt:
            #     self.cloneFrame(1)  # wait a bit before printing new prompt
            #     self.genPrompt(
            #         self.currRow, 1, 1
            #     )  # generate prompt right after printed text, i.e. 1 line below

            draw = ImageDraw.Draw(self.__frame)
            for _ in range(count):
                if self.__showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    draw.text(
                        (cx1, cy1), str(self.__cursor), self.__txtColor, self.__font
                    )
                self.__genFrame(self.__frame)
                if self.__showCursor:
                    cx1, cy1, _, _ = self.cursorToBox(
                        self.currRow, self.currCol, 1, 1, contin=True
                    )  # no unnecessary scroll
                    blankBoxImage = Image.new(
                        "RGB",
                        (self.__fontWidth, self.__fontHeight + self.__lineSpacing),
                        self.__bgColor,
                    )
                    self.__frame.paste(blankBoxImage, (cx1, cy1))
                    if (
                        self.__blinkCursor
                        and self.__frameCount % (self.__fps // 3) == 0
                    ):  # alter cursor such that blinks every one-third second
                        self.__alterCursor()

    def genPrompt(self, rowNum: int, colNum: int = 1, count: int = 1) -> None:
        origCursorState = self.__showCursor
        self.toggleShowCursor(True)
        self.genText(self.prompt, rowNum, colNum, count, False)
        self.__showCursor = origCursorState

    def scrollUp(self, count: int = 1) -> None:
        for _ in range(count):
            croppedFrame = self.__frame.crop(
                (0, self.__fontHeight + self.__lineSpacing, self.__width, self.__height)
            )  # make room for 1 extra line (__fontHeight + __lineSpacing)
            self.__frame = Image.new(
                "RGB", (self.__width, self.__height), self.__bgColor
            )
            self.__frame.paste(croppedFrame, (0, 0))
            self.currRow -= 1  # move cursor to where it was

            keys = list(self.__colInRow.keys())
            values = list(self.__colInRow.values())
            shiftedValues = values[1:] + [1]
            shiftedDict = dict(zip(keys, shiftedValues))
            self.__colInRow = shiftedDict
            ic(self.currRow, self.currCol)

    def deleteRow(self, rowNum: int) -> None:
        _, y1, _, _ = self.cursorToBox(
            rowNum, 1, 1, 1, True
        )  # continue = True; do not scroll up
        self.__colInRow[rowNum] = 1
        blankLineImage = Image.new(
            "RGB",
            (self.__width, self.__fontHeight + self.__lineSpacing),
            self.__bgColor,
        )
        self.__frame.paste(blankLineImage, (0, y1))
        ic(f"Deleted row {rowNum}")

    def genGif(self) -> None:
        os.system(
            f"ffmpeg -hide_banner -loglevel error -r {self.__fps} -i '{folderName}frame_%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' output.gif"
        )
        print(
            f"INFO: Generated GIF approximately {round(self.__frameCount / self.__fps, 2)}s long"
        )


# def replaceText(text: str, rowNum: int, colNum: int, count: int = 1) -> None:
#     global __frame
#     chars = 0
#     for _ in text:
#         chars += 1
#     layerImage = Image.new(
#         "RGB", (chars * __fontWidth, __fontHeight + __lineSpacing), __bgColor
#     )
#     x1, y1, _, _ = cursorToBox(rowNum, colNum)
#     __frame.paste(layerImage, (x1, y1))
#     genText(text, rowNum, colNum, count)
