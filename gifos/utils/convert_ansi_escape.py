# Colorscheme reference: https://github.com/rxyhn/yoru#art--colorscheme
from gifos.utils.load_config import ansi_escape_colors, gifos
from gifos.utils.schemas.ansi_escape import AnsiEscape


class ConvertAnsiEscape:
    __color_scheme = gifos.get("general", {}).get("color_scheme")

    @staticmethod
    def __get_color(color_dict, color_name, def_color):
        return (
            color_dict.get(color_name, def_color)
            if isinstance(color_dict, dict)
            else def_color
        )

    # fmt: off
    ANSI_ESCAPE_MAP_TXT_COLOR = {
        # normal color mode
        "30": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "black", "#232526"),
        "31": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "red", "#df5b61"),
        "32": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "green", "#78b892"),
        "33": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "yellow", "#de8f78"),
        "34": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "blue", "#6791c9"),
        "35": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "magenta", "#bc83e3"),
        "36": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "cyan", "#67afc1"),
        "37": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "white", "#e4e6e7"),
        "39": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("default_colors"), "fg", "#edeff0"),
        # bright color mode
        "90": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "black", "#2c2e2f"),
        "91": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "red", "#e8646a"),
        "92": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "green", "#81c19b"),
        "93": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "yellow", "#e79881"),
        "94": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "blue", "#709ad2"),
        "95": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "magenta", "#c58cec"),
        "96": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "cyan", "#70b8ca"),
        "97": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "white", "#f2f4f5"),
    }                                       

    ANSI_ESCAPE_MAP_BG_COLOR = {
        # normal color mode
        "40": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "black", "#232526"),
        "41": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "red", "#df5b61"),
        "42": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "green", "#78b892"),
        "43": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "yellow", "#de8f78"),
        "44": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "blue", "#6791c9"),
        "45": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "magenta", "#bc83e3"),
        "46": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "cyan", "#67afc1"),
        "47": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("normal_colors"), "white", "#e4e6e7"),
        "49": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("default_colors"), "bg", "#0c0e0f"),
        # bright color mode
        "100": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "black", "#2c2e2f"),
        "101": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "red", "#e8646a"),
        "102": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "green", "#81c19b"),
        "103": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "yellow", "#e79881"),
        "104": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "blue", "#709ad2"),
        "105": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "magenta", "#c58cec"),
        "106": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "cyan", "#70b8ca"),
        "107": __get_color(ansi_escape_colors.get(__color_scheme, {}).get("bright_colors"), "white", "#f2f4f5"),
    }
    # fmt: on

    @classmethod
    def convert(cls, escape_code) -> AnsiEscape:
        txt_color = cls.ANSI_ESCAPE_MAP_TXT_COLOR.get(escape_code)
        if txt_color:
            return AnsiEscape(data=txt_color, oper="txt_color")

        bg_color = cls.ANSI_ESCAPE_MAP_BG_COLOR.get(escape_code)
        if bg_color:
            return AnsiEscape(data=bg_color, oper="bg_color")

        return None
