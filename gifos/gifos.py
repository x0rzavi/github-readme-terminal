# TODO
# [] proper file paths
# [] incremental text effect
# [] profile image ascii art
# [] Better implementations for non monospace fonts
# [] Support all ANSI escape sequence forms
# [] Optimization + better code quality
# [] Documentation
# [] Test cases
# [] GIF maker implementation
# [] Scriptable input file

import os
from math import ceil
import random
import re
from pathlib import Path
from shutil import rmtree

from icecream import ic
from PIL import Image, ImageDraw, ImageFont

from gifos.utils.convert_ansi_escape import ConvertAnsiEscape
from gifos.utils.load_config import ansi_escape_colors, gifos

frame_base_name = gifos.get("files", {}).get("frame_base_name") or "frame_"
frame_folder_name = gifos.get("files", {}).get("frame_folder_name") or "./frames"
output_gif_name = gifos.get("files", {}).get("output_gif_name") or "output"

try:
    os.remove(output_gif_name + ".gif")
except Exception:
    pass

rmtree(frame_folder_name, ignore_errors=True)
os.mkdir(frame_folder_name)

font_path = Path(__file__).parent / "fonts"

class Terminal:
    def __init__(
        self,
        width: int,
        height: int,
        xpad: int,
        ypad: int,
        font_file: str = f"{font_path}/gohufont-uni-14.pil",
        font_size: int = 16,
    ) -> None:
        ic.configureOutput(includeContext=True)
        self.__width = width
        self.__height = height
        self.__xpad = xpad
        self.__ypad = ypad
        self.__font_file = font_file
        self.__font_size = font_size
        self.__debug = gifos.get("general", {}).get("debug") or False
        if not self.__debug:
            ic.disable()

        self.__txt_color = self.__def_txt_color = (
            ansi_escape_colors.get("default_colors", {}).get("fg")
            or ConvertAnsiEscape.convert("39").data
        )
        self.__bg_color = self.__def_bg_color = (
            ansi_escape_colors.get("default_colors", {}).get("bg")
            or ConvertAnsiEscape.convert("49").data
        )
        self.__frame_count = 0
        self.curr_row = 0
        self.curr_col = 0
        self.set_font(self.__font_file, self.__font_size)
        self.__cursor = gifos.get("general", {}).get("cursor") or "_"
        self.__cursor_orig = self.__cursor
        self.__show_cursor = gifos.get("general", {}).get("show_cursor") or True
        self.__blink_cursor = gifos.get("general", {}).get("blink_cursor") or True
        self.__fps = gifos.get("general", {}).get("fps") or 20
        self.__user_name = gifos.get("general", {}).get("user_name") or "x0rzavi"
        self.__prompt = (
            f"\x1b[0;91m{self.__user_name}\x1b[0m@\x1b[0;93mgifos ~> \x1b[0m"
        )
        self.__frame = self.__gen_frame()

    def set_txt_color(
        self,
        txt_color: str = ansi_escape_colors.get("default_colors", {}).get("fg")
        or ConvertAnsiEscape.convert("39").data,
    ) -> None:
        self.__txt_color = txt_color

    def set_bg_color(
        self,
        bg_color: str = ansi_escape_colors.get("default_colors", {}).get("bg")
        or ConvertAnsiEscape.convert("49").data,
    ) -> None:
        self.__bg_color = bg_color

    def __check_font_type(
        self, font_file: str, font_size: int
    ) -> ImageFont.ImageFont | ImageFont.FreeTypeFont | None:
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
            print(f"ERROR: Could not locate font_file {font_file}")
            return None

    def __check_monospace_font(
        self, font: ImageFont.ImageFont | ImageFont.FreeTypeFont
    ) -> dict:
        widths = [font.getbbox(chr(i))[2] for i in range(ord("A"), ord("Z") + 1)]
        avg_width = int(round(sum(widths) / len(widths), 0))
        return {"check": max(widths) == min(widths), "avg_width": avg_width}

    def set_font(self, font_file: str, font_size: int = 16) -> None:
        self.__font = self.__check_font_type(font_file, font_size)
        if self.__font:
            self.__line_spacing = 4
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
                ]  # rework
                font_metrics = self.__font.getmetrics()
                self.__font_height = font_metrics[0] + font_metrics[1]
            self.num_rows = (self.__height - 2 * self.__ypad) // (
                self.__font_height + self.__line_spacing
            )
            self.num_cols = (self.__width - 2 * self.__xpad) // (self.__font_width)
            print(f"INFO: Number of rows: {self.num_rows}")
            print(f"INFO: Number of columns: {self.num_cols}")
            self.__col_in_row = {_ + 1: 1 for _ in range(self.num_rows)}
            # self.clear_frame()
            ic(self.__font)  # debug
        else:
            exit(1)

    def toggle_show_cursor(self, choice: bool = None) -> None:
        self.__show_cursor = not self.__show_cursor if choice is None else choice
        ic(self.__show_cursor)  # debug

    def toggle_blink_cursor(self, choice: bool = None) -> None:
        self.__blink_cursor = not self.__blink_cursor if choice is None else choice
        ic(self.__blink_cursor)  # debug

    def __alter_cursor(self) -> None:
        self.__cursor = (
            self.__cursor_orig if self.__cursor != self.__cursor_orig else " "
        )
        ic(self.__cursor)  # debug

    def __check_multiline(self, text: str | list) -> bool:  # make local to gen_text() ?
        if isinstance(text, list):
            if len(text) <= 1:
                return False
        elif isinstance(text, str):
            return "\n" in text
        return True

    def __frame_debug_lines(self, frame: Image.Image) -> Image.Image:
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

    def clear_frame(self) -> None:
        self.__frame = self.__gen_frame()
        ic("Frame cleared")

    def clone_frame(self, count: int = 1) -> None:
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
                if first_blank_row < max_row_num:  # needed ?
                    ic("NEEDED!")  # debug
                    exit(1)
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
        if prompt and contin:  # why ?
            print("ERROR: Both prompt and contin can't be simultaneously True")  # debug
            exit(1)

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
                        # print(code)
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
        # speed configuration
        # 0 - random - random frame count
        # 1 - fast - 1 frame count
        # 2 - medium - 2 frame count
        # 3 - slow - 3 frame count
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
        self.__prompt = prompt

    def gen_prompt(self, row_num: int, col_num: int = 1, count: int = 1) -> None:
        self.clone_frame(1)  # wait a bit before printing new prompt
        orig_cursor_state = self.__show_cursor
        self.toggle_show_cursor(True)
        self.gen_text(
            self.__prompt, row_num, col_num, count, False, False
        )  # generate prompt right after printed text, i.e. 1 line below
        self.__show_cursor = orig_cursor_state

    def scroll_up(self, count: int = 1) -> None:
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
                print("ERROR: Image exceeds frame dimensions")
                exit(1)
            for i in range(rows_covered):
                self.__col_in_row[row_num + i] = cols_covered
            self.image_col = col_num + cols_covered  # helper for scripts
            self.__frame.paste(image, (x1, y1))
            self.__gen_frame(self.__frame)

    def set_fps(self, fps: float) -> None:
        self.__fps = fps

    def gen_gif(self) -> None:
        os.system(
            f"ffmpeg -hide_banner -loglevel error -r {self.__fps} -i '{frame_folder_name}/{frame_base_name}%d.png' -filter_complex '[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse' {output_gif_name}.gif"
        )
        print(
            f"INFO: Generated {output_gif_name}.gif approximately {round(self.__frame_count / self.__fps, 2)}s long"
        )
