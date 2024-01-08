# TODO:
# [] Documentation
# [] proper file paths
# [] incremental text effect
# [] Better implementations for non monospace fonts
# [] Support all ANSI escape sequence forms
# [] Optimization + better code quality
# [] Test cases
# [] GIF maker implementation
# [] Scriptable input file

import os
from math import ceil
from pathlib import Path
import random
import re
from shutil import rmtree
import sys

from icecream import ic
from PIL import Image, ImageDraw, ImageFont

from gifos.utils.convert_ansi_escape import ConvertAnsiEscape
from gifos.utils.load_config import gifos_settings

frame_base_name = gifos_settings.get("files", {}).get("frame_base_name") or "frame_"
frame_folder_name = gifos_settings.get("files", {}).get("frame_folder_name") or "./frames"
output_gif_name = gifos_settings.get("files", {}).get("output_gif_name") or "output"

try:
    os.remove(output_gif_name + ".gif")
except Exception:
    pass

rmtree(frame_folder_name, ignore_errors=True)
os.mkdir(frame_folder_name)

font_path = Path(__file__).parent / "fonts"


class Terminal:
    """A class to represent a terminal.

    This class represents a terminal with a specified width, height, padding, and font.

    Attributes:
        width: The width of the terminal.
        height: The height of the terminal.
        xpad: The horizontal padding of the terminal.
        ypad: The vertical padding of the terminal.
        font_file: The file path of the font to use for the terminal. Defaults to "gohufont-uni-14.pil".
        font_size: The size of the font to use for the terminal. Defaults to 16.
        line_spacing: The line spacing to use for the terminal. Defaults to 4.
        curr_row: The current row of the cursor in terminal.
        curr_col: The current column of the cursor in terminal.
        num_rows: The number of rows in the terminal.
        num_cols: The number of columns in the terminal.
        image_col: The column number of the last image pasted in the terminal.

    Methods:
        set_txt_color: Set the text color to be used.
        set_bg_color: Set the background color to be used.
        set_font: Set the font to be used.
        toggle_show_cursor: Toggle the visibility of the cursor.
        toggle_blink_cursor: Toggle the blinking of the cursor.
        save_frame: Save the current frame of the terminal.
        clear_frame: Clear the current frame of the terminal.
        clone_frame: Clone the current frame of the terminal.
        cursor_to_box: Move the cursor to a specified box (coordinate) in the terminal.
        gen_text: Generate text on the terminal.
        gen_typing_text: Generate text on the terminal as if it is being typed.
        set_prompt: Set the prompt text to be used.
        gen_prompt: Generate the prompt text on the terminal.
        scroll_up: Scroll up the terminal.
        delete_row: Delete a row in the terminal.
        paste_image: Paste an image on the terminal.
        set_fps: Set the FPS of the GIF to be generated.
        gen_gif: Generate the GIF from the frames.
    """

    def __init__(
        self,
        width: int,
        height: int,
        xpad: int,
        ypad: int,
        font_file: str = f"{font_path}/gohufont-uni-14.pil",
        font_size: int = 16,
        line_spacing: int = 4,
    ) -> None:
        """Initialize a Terminal object.

        :param width: The width of the terminal.
        :type width: int
        :param height: The height of the terminal.
        :type height: int
        :param xpad: The horizontal padding of the terminal.
        :type xpad: int
        :param ypad: The vertical padding of the terminal.
        :type ypad: int
        :param font_file: The file path of the font to use for the terminal.
        :type font_file: str, optional
        :param font_size: The size of the font to use for the terminal. Defaults to 16.
        :type font_size: int, optional
        :param line_spacing: The line spacing to use for the terminal. Defaults to 4.
        :type line_spacing: int, optional
        """
        ic.configureOutput(includeContext=True)
        self.__width = width
        self.__height = height
        self.__xpad = xpad
        self.__ypad = ypad
        self.__font_file = font_file
        self.__font_size = font_size
        self.__debug = gifos_settings.get("general", {}).get("debug") or False
        if not self.__debug:
            ic.disable()

        self.__txt_color = self.__def_txt_color = ConvertAnsiEscape.convert("39").data
        self.__bg_color = self.__def_bg_color = ConvertAnsiEscape.convert("49").data
        self.__frame_count = 0
        self.curr_row = 0
        self.curr_col = 0
        self.set_font(self.__font_file, self.__font_size, line_spacing)
        self.__cursor = gifos_settings.get("general", {}).get("cursor") or "_"
        self.__cursor_orig = self.__cursor
        self.__show_cursor = gifos_settings.get("general", {}).get("show_cursor", True)
        self.__blink_cursor = gifos_settings.get("general", {}).get("blink_cursor", True)
        self.__fps = gifos_settings.get("general", {}).get("fps") or 20
        self.__loop_count = gifos_settings.get("general", {}).get("loop_count") or 0
        self.__user_name = gifos_settings.get("general", {}).get("user_name") or "x0rzavi"
        self.__prompt = (
            f"\x1b[0;91m{self.__user_name}\x1b[0m@\x1b[0;93mgifos ~> \x1b[0m"
        )
        self.__frame = self.__gen_frame()

    def set_txt_color(
        self,
        txt_color: str = ConvertAnsiEscape.convert("39").data,
    ) -> None:
        """Set the text color to be used in the Terminal object.

        This method sets the text color of the Terminal object.

        :param txt_color: The text color to set.
        :type txt_color: str, optional
        """
        self.__txt_color = txt_color

    def set_bg_color(
        self,
        bg_color: str = ConvertAnsiEscape.convert("49").data,
    ) -> None:
        """Set the background color to be used in the Terminal object.

        This method sets the background color of the Terminal object.

        :param bg_color: The text color to set.
        :type bg_color: str, optional
        """
        self.__bg_color = bg_color

    def __check_font_type(
        self, font_file: str, font_size: int
    ) -> ImageFont.ImageFont | ImageFont.FreeTypeFont | None:
        """Check the type of the font file and return the appropriate font object.

        This method checks the type of the font file specified by `font_file`. If the font file is a TrueType font, it returns an `ImageFont.truetype` object with the specified `font_size`. If the font file is a bitmap font, it returns an `ImageFont.load` object and ignores the `font_size`. If the font file is neither a TrueType font nor a bitmap font, it returns `None`.

        :param font_file: The file path of the font file.
        :type font_file: str
        :param font_size: The size of the font.
        :type font_size: int
        :return: An `ImageFont.truetype` object if the font file is a TrueType font, an `ImageFont.load` object if the font file is a bitmap font, or `None` if the font file is neither a TrueType font nor a bitmap font.
        :rtype: ImageFont.ImageFont | ImageFont.FreeTypeFont | None
        """
        try:
            font = ImageFont.truetype(font_file, font_size)
            return font
        except OSError:
            pass

        try:
            font = ImageFont.load(font_file)
            print(f"WARNING: {font_file} is BitMap - Ignoring size {font_size}")
            return font
        except OSError:
            return None

    def __check_monospace_font(
        self, font: ImageFont.ImageFont | ImageFont.FreeTypeFont
    ) -> dict:
        """Check if the specified font is monospaced and return a dictionary with the
        check result and the average width of the characters.

        This method checks if the specified font is monospaced by comparing the widths of the uppercase letters A-Z. If all the letters have the same width, the font is considered monospaced. The method returns a dictionary with the check result and the average width of the characters.

        :param font: The font to check.
        :type font: ImageFont.ImageFont | ImageFont.FreeTypeFont
        :return: A dictionary with the check result and the average width of the characters. The dictionary has the following keys:
            - "check": A boolean that is `True` if the font is monospaced and `False` otherwise.
            - "avg_width": The average width of the characters in the font.
        :rtype: dict
        """
        widths = [font.getbbox(chr(i))[2] for i in range(ord("A"), ord("Z") + 1)]
        avg_width = int(round(sum(widths) / len(widths), 0))
        return {"check": max(widths) == min(widths), "avg_width": avg_width}

    def set_font(
        self, font_file: str, font_size: int = 16, line_spacing: int = 4
    ) -> None:
        """Set the font to be used for the Terminal object.

        This method sets the font of the Terminal object. The font is specified by a
        file path and a size. The method also sets the line spacing of the terminal. If
        the font is monospaced, the method sets the width and height of the font to the
        width and height of the widest and tallest characters, respectively. If the font
        is not monospaced, the method sets the width of the font to the average width of
        the characters and the height of the font to the sum of the ascent and descent
        of the font. The method also calculates the number of rows and columns that can
        fit in the terminal based on the font size and line spacing.

        :param font_file: The file path of the font file.
        :type font_file: str
        :param font_size: The size of the font. Defaults to 16.
        :type font_size: int, optional
        :param line_spacing: The line spacing to use for the terminal. Defaults to 4.
        :type line_spacing: int, optional
        """
        self.__font = self.__check_font_type(font_file, font_size)
        if self.__font:
            self.__line_spacing = line_spacing
            if self.__check_monospace_font(self.__font)["check"]:
                self.__font_width = self.__font.getbbox("W")[
                    2
                ]  # empirically widest character
                self.__font_height = self.__font.getbbox(r'|(/QMW"')[
                    3
                ]  # empirically tallest characters
            else:
                self.__font_width = self.__check_monospace_font(self.__font)[
                    "avg_width"
                ]  # FIXME: rework
                font_metrics = self.__font.getmetrics()
                self.__font_height = font_metrics[0] + font_metrics[1]
            self.num_rows = (self.__height - 2 * self.__ypad) // (
                self.__font_height + self.__line_spacing
            )
            self.num_cols = (self.__width - 2 * self.__xpad) // (self.__font_width)
            print(f"INFO: Loaded font_file: {font_file}")
            print(f"INFO: Number of rows: {self.num_rows}")
            print(f"INFO: Number of columns: {self.num_cols}")
            self.__col_in_row = {_ + 1: 1 for _ in range(self.num_rows)}
            # self.clear_frame()
            ic(self.__font)  # debug
        else:
            print(f"ERROR: Could not locate font_file {font_file}")
            sys.exit(1)

    def toggle_show_cursor(self, choice: bool = None) -> None:
        """Toggle the visibility of the cursor in the Terminal object.

        This method toggles the visibility of the cursor in the Terminal object. If `choice` is `None`, the method toggles the current visibility of the cursor. If `choice` is `True`, the method makes the cursor visible. If `choice` is `False`, the method makes the cursor invisible.

        :param choice: The desired visibility of the cursor. If `None`, the method toggles the current visibility of the cursor. If `True`, the method makes the cursor visible. If `False`, the method makes the cursor invisible. Defaults to `None`.
        :type choice: bool, optional
        """
        self.__show_cursor = not self.__show_cursor if choice is None else choice
        ic(self.__show_cursor)  # debug

    def toggle_blink_cursor(self, choice: bool = None) -> None:
        """Toggle the blinking of the cursor in the Terminal object.

        This method toggles the blinking of the cursor in the Terminal object. If `choice` is `None`, the method toggles the current blinking state of the cursor. If `choice` is `True`, the method makes the cursor blink. If `choice` is `False`, the method makes the cursor stop blinking.

        :param choice: The desired blinking state of the cursor. If `None`, the method toggles the current blinking state of the cursor. If `True`, the method makes the cursor blink. If `False`, the method makes the cursor stop blinking. Defaults to `None`.
        :type choice: bool, optional
        """
        self.__blink_cursor = not self.__blink_cursor if choice is None else choice
        ic(self.__blink_cursor)  # debug

    def __alter_cursor(self) -> None:
        """Alter the cursor of the Terminal object.

        This method alters the cursor of the Terminal object. If the current cursor is
        not the original cursor, the method sets the cursor to the original cursor;
        otherwise, it sets the cursor to a space.
        """
        self.__cursor = (
            self.__cursor_orig if self.__cursor != self.__cursor_orig else " "
        )
        ic(self.__cursor)  # debug

    def __check_multiline(
        self, text: str | list
    ) -> bool:  # FIXME: make local to gen_text() ?
        """Check if the input text is multiline.

        This method checks if the input text is multiline. If the text is a list and has more than one element, the method returns `True`. If the text is a string and contains a newline character, the method returns `True`. In all other cases, the method returns `False`.

        :param text: The text to check. Can be a string or a list of strings.
        :type text: str | list
        :return: `True` if the text is multiline, `False` otherwise.
        :rtype: bool
        """
        if isinstance(text, list):
            if len(text) <= 1:
                return False
        elif isinstance(text, str):
            return "\n" in text
        return True

    def __frame_debug_lines(self, frame: Image.Image) -> Image.Image:
        """Add debug lines to a frame.

        This method adds debug lines to a frame. The frame is specified by `frame`. The method draws horizontal and vertical lines on the frame to represent rows and columns, respectively. It also draws a red border around the frame. The row and column numbers are printed next to the corresponding lines. The method returns the frame with the added debug lines.

        :param frame: The frame to add debug lines to.
        :type frame: Image.Image
        :return: The frame with the added debug lines.
        :rtype: Image.Image
        """
        # checker box to debug
        draw = ImageDraw.Draw(frame)
        for i in range(self.num_rows + 1):  # (n + 1) lines
            x1 = self.__xpad
            x2 = self.__width - self.__xpad
            y1 = y2 = self.__ypad + i * (self.__font_height + self.__line_spacing)
            draw.line([(x1, y1), (x2, y2)], "yellow")
            draw.text((0, y1), str(i + 1), "orange", self.__font)  # row numbers
        for i in range(self.num_cols + 1):  # (n + 1) lines
            x1 = x2 = self.__xpad + i * self.__font_width
            y1 = self.__ypad
            y2 = self.__height - self.__ypad
            draw.line([(x1, y1), (x2, y2)], "turquoise")
        draw.line(
            [(self.__xpad, self.__ypad), (self.__width - self.__xpad, self.__ypad)],
            "red",
        )  # top
        draw.line(
            [(self.__xpad, self.__ypad), (self.__xpad, self.__height - self.__ypad)],
            "red",
        )  # left
        draw.line(
            [
                (self.__xpad, self.__height - self.__ypad),
                (self.__width - self.__xpad, self.__height - self.__ypad),
            ],
            "red",
        )  # bottom
        draw.line(
            [
                (self.__width - self.__xpad, self.__ypad),
                (self.__width - self.__xpad, self.__height - self.__ypad),
            ],
            "red",
        )  # right
        return frame

    def __gen_frame(self, frame: Image.Image = None) -> Image.Image:
        """Generate a new frame or save the current frame.

        This method generates a new frame if `frame` is `None` or saves the current frame if `frame` is not `None`. If a new frame is generated, the method initializes the frame with the background color, sets the number of columns in each row to 1, and moves the cursor to the box at (1, 1). If the debug mode is on, the method also draws debug lines on the frame. If the current frame is saved, the method increments the frame count, saves the frame as a PNG file with a name based on the frame count.

        :param frame: The current frame. If `None`, a new frame is generated. If not `None`, the current frame is saved. Defaults to `None`.
        :type frame: Image.Image, optional
        :return: The new or saved frame.
        :rtype: Image.Image
        """
        if frame is None:
            frame = Image.new("RGB", (self.__width, self.__height), self.__bg_color)
            self.__col_in_row = {_ + 1: 1 for _ in range(self.num_rows)}
            if self.__debug:
                frame = self.__frame_debug_lines(frame)
            self.cursor_to_box(1, 1)  # initialize at box (1, 1)
            return frame
        self.__frame_count += 1
        file_name = frame_base_name + str(self.__frame_count) + ".png"
        frame.save(frame_folder_name + "/" + file_name, "PNG")
        print(f"INFO: Generated frame #{self.__frame_count}")  # debug
        return frame

    def save_frame(self, base_file_name: str):
        """Save the current frame as a PNG file.

        This method saves the current frame as a PNG file. The file name is based on `base_file_name`.

        :param base_file_name: The base file name for the PNG file.
        :type base_file_name: str
        """
        file_name = base_file_name + ("" if ".png" in base_file_name else ".png")
        self.__frame.save(file_name, "PNG")
        print(f"INFO: Saved frame #{self.__frame_count}: {file_name}")

    def clear_frame(self) -> None:
        """Clear the current frame.

        This method clears the current frame by generating a new frame. The new frame is
        initialized with the background color, the number of columns in each row is set
        to 1, and the cursor is moved to the box at (1, 1).
        """
        self.__frame = self.__gen_frame()
        ic("Frame cleared")

    def clone_frame(self, count: int = 1) -> None:
        """Clone the current frame a specified number of times.

        This method clones the current frame a specified number of times. The number of times to clone the frame is specified by `count`.

        :param count: The number of times to clone the frame. Defaults to 1.
        :type count: int, optional
        """
        for _ in range(count):
            self.__frame = self.__gen_frame(self.__frame)
        ic(f"Frame cloned {count} times")

    def cursor_to_box(
        self,
        row_num: int,
        col_num: int,
        text_num_lines: int = 1,
        text_num_chars: int = 1,
        contin: bool = False,
        force_col: bool = False,  # to assist in delete_row()
    ) -> tuple:
        """Move the cursor to a specific box (coordinate) in the Terminal object.

        This method moves the cursor to a specific box in the Terminal object. The box is specified by `row_num` and `col_num`. The method also takes into account the number of lines and characters in the text that will be printed at the box. If `contin` is `True`, the method continues printing from the current position of the cursor. If `force_col` is `True`, the method forces the cursor to move to the specified column.

        :param row_num: The row number of the box.
        :type row_num: int
        :param col_num: The column number of the box.
        :type col_num: int
        :param text_num_lines: The number of lines in the text that will be printed at the box. Defaults to 1.
        :type text_num_lines: int, optional
        :param text_num_chars: The number of characters in the text that will be printed at the box. Defaults to 1.
        :type text_num_chars: int, optional
        :param contin: Whether to continue printing from the current position of the cursor. Defaults to False.
        :type contin: bool, optional
        :param force_col: Whether to force the cursor to move to the specified column. Defaults to False.
        :type force_col: bool, optional
        :return: The coordinates of the box.
        :rtype: tuple
        """
        if row_num < 1 or col_num < 1:  # do not care about exceeding col_num
            raise ValueError
        elif row_num > self.num_rows:
            ic(
                f"row {row_num} > max row {self.num_rows}, using row {self.num_rows} instead"
            )
            row_num = self.num_rows
        max_row_num = (
            self.num_rows - text_num_lines + 1
        )  # maximum row that can be permitted
        min_col_num = self.__col_in_row[row_num]

        if not contin:
            num_blank_rows = 0
            first_blank_row = self.num_rows + 1  # all rows are filled
            for i in range(self.num_rows, row_num - 1, -1):
                if self.__col_in_row[i] == 1:
                    first_blank_row = i
                    num_blank_rows += 1
                else:
                    break
            ic(first_blank_row, num_blank_rows)  # debug

            if row_num > max_row_num:
                ic(f"{text_num_lines} lines cannot be accomodated at {row_num}")
                ic(f"Maximum possible is {max_row_num}")
                if first_blank_row < max_row_num:  # FIXME: needed ?
                    ic("NEEDED!")  # debug
                    sys.exit(1)
                    scroll_times = text_num_lines - num_blank_rows
                    ic(scroll_times)
                    self.scroll_up(scroll_times)
                    row_num = self.curr_row
                else:
                    row_num = max_row_num  # enough space to print; no need to scroll

            elif first_blank_row > row_num:
                scroll_times = first_blank_row - row_num
                ic(scroll_times)
                self.scroll_up(scroll_times)
        else:
            if col_num < min_col_num and not force_col:
                ic(f"{text_num_chars} chars cannot be accomodated at column {col_num}")
                col_num = self.__col_in_row[row_num]
        self.curr_row, self.curr_col = row_num, col_num
        ic(self.curr_row, self.curr_col)  # debug

        x1 = self.__xpad + (col_num - 1) * self.__font_width
        y1 = self.__ypad + (row_num - 1) * (self.__font_height + self.__line_spacing)
        x2 = self.__xpad + col_num * self.__font_width
        y2 = self.__ypad + row_num * (self.__font_height + self.__line_spacing)
        return x1, y1, x2, y2

    def gen_text(
        self,
        text: str | list,
        row_num: int,
        col_num: int = 1,
        count: int = 1,
        prompt: bool = False,
        contin: bool = False,
    ) -> None:
        """Generate text on the Terminal object.

        This method generates text on the Terminal object. The text is specified by `text`, and the position of the text is specified by `row_num` and `col_num`. The method also takes into account whether to generate a prompt after the text (`prompt`), whether to continue printing from the current position of the cursor (`contin`), and the number of times to generate the text (`count`).
        If there is a single line of text, the default behaviour to position the cursor is at the end of the same line.
        If there are multiple lines of text, the default behaviour to position the cursor is at the beginning of the next line.
        Prompt is generated only if there are multiple lines of text.

        :param text: The text to generate. If a string, the text is split into lines. If a list, each element is treated as a line of text.
        :type text: str | list
        :param row_num: The row number where the text starts.
        :type row_num: int
        :param col_num: The column number where the text starts. Defaults to 1.
        :type col_num: int, optional
        :param count: The number of times to generate the text. Defaults to 1.
        :type count: int, optional
        :param prompt: Whether to generate a prompt after the text. Defaults to False.
        :type prompt: bool, optional
        :param contin: Whether to continue printing from the current position of the cursor. Defaults to False.
        :type contin: bool, optional
        """
        if prompt and contin:  # FIXME: why ?
            print("ERROR: Both prompt and contin can't be simultaneously True")  # debug
            sys.exit(1)

        if isinstance(text, str):
            text_lines = text.splitlines()
            text_num_lines = len(text_lines)
        else:
            text_lines = text
            text_num_lines = len(text)

        ansi_escape_pattern = re.compile(
            r"(\\x1b\[\d+(?:;\d+)*m|\x1b\[\d+(?:;\d+)*m)"
        )  # match ANSI color mode escape codes
        color_code_pattern = re.compile(
            r"\\x1b\[(\d+)(?:;(\d+))*m|\x1b\[(\d+)(?:;(\d+))*m"
        )  # match only color codes
        for i in range(text_num_lines):  # for each line
            self.cursor_to_box(
                row_num + i,
                col_num,
                1,
                1,
                contin,
            )  # initialize position to check contin for each line

            line = text_lines[i]  # single line
            words = [word for word in re.split(ansi_escape_pattern, line) if word]
            for word in words:  # for each word in line
                if re.match(ansi_escape_pattern, word):  # if ANSI escape sequence
                    codes = [
                        code
                        for _ in re.findall(color_code_pattern, word)
                        for code in _
                        if code
                    ]
                    for code in codes:
                        if code == "0":  # reset to default
                            self.set_txt_color()
                            self.set_bg_color()
                            continue
                        else:
                            code_info = ConvertAnsiEscape.convert(code)
                            if code_info:
                                if code_info.oper == "txt_color":
                                    self.set_txt_color(code_info.data)
                                    continue
                                if code_info.oper == "bg_color":
                                    self.set_bg_color(code_info.data)
                                    continue
                else:  # if normal word
                    text_num_chars = len(word)
                    x1, y1, _, _ = self.cursor_to_box(
                        row_num + i,
                        col_num,
                        1,
                        text_num_chars,
                        True,  # contin=True since words in same line
                    )
                    draw = ImageDraw.Draw(self.__frame)
                    _, _, rx2, _ = draw.textbbox(
                        (x1, y1), word, self.__font
                    )  # change bg_color
                    draw.rectangle(
                        (x1, y1, rx2, y1 + self.__font_height), self.__bg_color
                    )
                    draw.text((x1, y1), word, self.__txt_color, self.__font)
                    self.curr_col += len(word)
                    self.__col_in_row[self.curr_row] = self.curr_col
                    ic(self.curr_row, self.curr_col)  # debug
        if self.__check_multiline(text_lines):
            self.cursor_to_box(
                self.curr_row + 1, 1, 1, 1, contin
            )  # move down by 1 row only if multiline

        if prompt and self.__check_multiline(
            text_lines
        ):  # only generate prompt if multiline
            self.gen_prompt(self.curr_row, 1, 1)

        draw = ImageDraw.Draw(self.__frame)
        for _ in range(count):
            if self.__show_cursor:
                cx1, cy1, _, _ = self.cursor_to_box(
                    self.curr_row, self.curr_col, 1, 1, contin=True
                )  # no unnecessary scroll
                draw.text(
                    (cx1, cy1), str(self.__cursor), self.__def_txt_color, self.__font
                )
            self.__gen_frame(self.__frame)
            if self.__show_cursor:
                cx1, cy1, _, _ = self.cursor_to_box(
                    self.curr_row, self.curr_col, 1, 1, contin=True
                )  # no unnecessary scroll
                blank_box_image = Image.new(
                    "RGB",
                    (self.__font_width, self.__font_height + self.__line_spacing),
                    self.__def_bg_color,
                )
                self.__frame.paste(blank_box_image, (cx1, cy1))
                if (
                    self.__blink_cursor and self.__frame_count % (self.__fps // 3) == 0
                ):  # alter cursor such that blinks every one-third second
                    self.__alter_cursor()

    def gen_typing_text(
        self,
        text: str,
        row_num: int,
        col_num: int = 1,
        contin: bool = False,
        speed: int = 0,
    ) -> None:
        """Generate typing text simulation on the Terminal object.

        This method generates typing text on the Terminal object. The text is specified by `text`, and the position of the text is specified by `row_num` and `col_num`. The method also takes into account whether to continue printing from the current position of the cursor `contin`, and the speed of typing `speed`.

        Speed configuration:
        0 - random - random frame count
        1 - fast - 1 frame count
        2 - medium - 2 frame count
        3 - slow - 3 frame count

        :param text: The text to generate. If a string, the text is split into words and each word is printed character by character.
        :type text: str
        :param row_num: The row number where the text starts.
        :type row_num: int
        :param col_num: The column number where the text starts. Defaults to 1.
        :type col_num: int, optional
        :param contin: Whether to continue printing from the current position of the cursor. Defaults to False.
        :type contin: bool, optional
        :param speed: The speed of typing. Can be 0 (random), 1 (fast), 2 (medium), or 3 (slow). Defaults to 0.
        :type speed: int, optional
        """
        ansi_escape_pattern = re.compile(
            r"(\\x1b\[\d+(?:;\d+)*m|\x1b\[\d+(?:;\d+)*m)"
        )  # match ANSI color mode escape codes
        if not contin:
            self.cursor_to_box(row_num, col_num, 1, 1, contin)
        words = [word for word in re.split(ansi_escape_pattern, text) if word]
        for word in words:
            if re.match(ansi_escape_pattern, word):
                self.gen_text(word, row_num, self.__col_in_row[row_num], 0, False, True)
            else:
                for char in word:
                    count = speed if speed in [1, 2, 3] else random.choice([1, 2, 3])
                    self.gen_text(
                        char, row_num, self.__col_in_row[row_num], count, False, True
                    )

    def set_prompt(self, prompt: str) -> None:
        """Set the prompt for the Terminal object.

        This method sets the prompt for the Terminal object. The prompt is specified by `prompt`.

        :param prompt: The prompt to set.
        :type prompt: str
        """
        self.__prompt = prompt

    def gen_prompt(self, row_num: int, col_num: int = 1, count: int = 1) -> None:
        """Generate a prompt on the Terminal object.

        This method generates a prompt on the Terminal object. The position of the prompt is specified by `row_num` and `col_num`, and the number of times to generate the prompt is specified by `count`. Before generating the prompt, the method clones the current frame and ensures that the cursor is visible. After generating the prompt, the method restores the original state of the cursor.

        :param row_num: The row number where the prompt starts.
        :type row_num: int
        :param col_num: The column number where the prompt starts. Defaults to 1.
        :type col_num: int, optional
        :param count: The number of times to generate the prompt. Defaults to 1.
        :type count: int, optional
        """
        self.clone_frame(1)  # wait a bit before printing new prompt
        orig_cursor_state = self.__show_cursor
        self.toggle_show_cursor(True)
        self.gen_text(
            self.__prompt, row_num, col_num, count, False, False
        )  # generate prompt right after printed text, i.e. 1 line below
        self.__show_cursor = orig_cursor_state

    def scroll_up(self, count: int = 1) -> None:
        """Scroll up the Terminal object.

        This method scrolls up the Terminal object a specified number of times. The number of times to scroll up is specified by `count`.

        :param count: The number of times to scroll up. Defaults to 1.
        :type count: int, optional
        """
        for _ in range(count):
            cropped_frame = self.__frame.crop(
                (
                    0,
                    self.__font_height + self.__line_spacing,
                    self.__width,
                    self.__height,
                )
            )  # make room for 1 extra line (__font_height + __line_spacing)
            self.__frame = Image.new(
                "RGB", (self.__width, self.__height), self.__def_bg_color
            )
            self.__frame.paste(cropped_frame, (0, 0))
            self.curr_row -= 1  # move cursor to where it was

            keys = list(self.__col_in_row.keys())
            values = list(self.__col_in_row.values())
            shifted_values = values[1:] + [1]
            shifted_dict = dict(zip(keys, shifted_values))
            self.__col_in_row = shifted_dict
            ic(self.curr_row, self.curr_col)

    def delete_row(self, row_num: int, col_num: int = 1) -> None:
        """Delete a row in the Terminal object.

        This method deletes a row in the Terminal object. The row is specified by `row_num`, and the column where the deletion starts is specified by `col_num`.

        :param row_num: The row number to delete.
        :type row_num: int
        :param col_num: The column number where the deletion starts. Defaults to 1.
        :type col_num: int, optional
        """
        x1, y1, _, _ = self.cursor_to_box(
            row_num, col_num, 1, 1, True, force_col=True
        )  # continue = True; do not scroll up
        self.__col_in_row[row_num] = col_num
        blank_line_image = Image.new(
            "RGB",
            (self.__width - x1, self.__font_height + self.__line_spacing),
            self.__bg_color,
        )
        self.__frame.paste(blank_line_image, (x1, y1))
        ic(f"Deleted row {row_num} starting at col {col_num}")

    def paste_image(
        self,
        image_file: str,
        row_num: int,
        col_num: int = 1,
        size_multiplier: float = 1,
    ) -> None:
        """Paste an image onto the Terminal object.

        This method pastes an image onto the Terminal object. The image is specified by `image_file`, and the position of the image is specified by `row_num` and `col_num`. The method also takes into account a size multiplier `size_multiplier` to resize (with same aspect ratio) the image before pasting it.

        :param image_file: The path to the image file to paste.
        :type image_file: str
        :param row_num: The row number where the image starts.
        :type row_num: int
        :param col_num: The column number where the image starts. Defaults to 1.
        :type col_num: int, optional
        :param size_multiplier: The multiplier by which to resize the image. Defaults to 1.
        :type size_multiplier: float, optional
        """
        x1, y1, _, _ = self.cursor_to_box(row_num, col_num, 1, 1, True, True)
        with Image.open(image_file) as image:
            image_width, image_height = image.size
            image = image.resize(
                (
                    int(image_width * size_multiplier),
                    int(image_height * size_multiplier),
                )
            )
            rows_covered = ceil(
                image.height / (self.__font_height + self.__line_spacing)
            )
            cols_covered = ceil(image.width / (self.__font_width)) + 1
            if (
                row_num + rows_covered > self.num_rows
                or col_num + cols_covered > self.num_cols
            ):
                print("WARNING: Image exceeds frame dimensions")
            else:
                for i in range(rows_covered):
                    self.__col_in_row[row_num + i] = cols_covered
                self.image_col = col_num + cols_covered  # helper for scripts
                self.__frame.paste(image, (x1, y1))
                self.__gen_frame(self.__frame)

    def set_fps(self, fps: float) -> None:
        """Set the frames per second (fps) for the GIF to be generated.

        This method sets the frames per second (fps) for the GIF to be generated. The fps is specified by `fps`.

        :param fps: The frames per second to set.
        :type fps: float
        """
        self.__fps = fps

    def set_loop_count(self, loop_count: int) -> None:
        """Set the loop count for GIF to be generated.

        This method sets the loop count for the GIF to be generated. Specifications for the loop number
        are given by ffmpeg as follows:
             -1:        No-loop (stop after first playback)
             0:         Infinite loop
             1..65535:  Loop n times up to a maximum of 65535

        :param loop_count: The number of loops in the GIF to be generated.
        :type loop_count: int
        """
        def limit(n: int, lower: int, upper: int):
            return min(max(n, lower), upper)

        self.__loop_count = limit(loop_count, -1, 65535)

    def gen_gif(self) -> None:
        """Generate a GIF from the frames.

        This method generates a GIF from the frames. The method uses the `ffmpeg` command to generate the GIF, with the frames per second (fps) set to the fps specified in the Terminal object. The generated GIF is saved with the name specified by `output_gif_name`.
        """
        os.system(
            f"ffmpeg -hide_banner -loglevel error -r {self.__fps} -i '{frame_folder_name}/{frame_base_name}%d.png' -loop {self.__loop_count} -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' {output_gif_name}.gif"
        )
        print(
            f"INFO: Generated {output_gif_name}.gif approximately {round(self.__frame_count / self.__fps, 2)}s long"
        )
