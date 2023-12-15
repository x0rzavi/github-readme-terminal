# Colorscheme reference: https://github.com/rxyhn/yoru#art--colorscheme
from .schemas.ansiEscape import ansiEscape
from .load_config import ansi_escape_colors


class convertAnsiEscape:
    @staticmethod
    def __getColor(colorDict, colorName, defColor):
        return (
            colorDict.get(colorName, defColor)
            if isinstance(colorDict, dict)
            else defColor
        )

    ANSI_ESCAPE_MAP_TXT_COLOR = {
        # normal color mode
        "30": __getColor(ansi_escape_colors.get("normalColors"), "black", "#232526"),
        "31": __getColor(ansi_escape_colors.get("normalColors"), "red", "#df5b61"),
        "32": __getColor(ansi_escape_colors.get("normalColors"), "green", "#78b892"),
        "33": __getColor(ansi_escape_colors.get("normalColors"), "yellow", "#de8f78"),
        "34": __getColor(ansi_escape_colors.get("normalColors"), "blue", "#6791c9"),
        "35": __getColor(ansi_escape_colors.get("normalColors"), "magenta", "#bc83e3"),
        "36": __getColor(ansi_escape_colors.get("normalColors"), "cyan", "#67afc1"),
        "37": __getColor(ansi_escape_colors.get("normalColors"), "white", "#e4e6e7"),
        "39": __getColor(ansi_escape_colors.get("defaultColors"), "fg", "#F2F4F5"),
        # bright color mode
        "90": __getColor(ansi_escape_colors.get("brightColors"), "black", "#2c2e2f"),
        "91": __getColor(ansi_escape_colors.get("brightColors"), "red", "#e8646a"),
        "92": __getColor(ansi_escape_colors.get("brightColors"), "green", "#81c19b"),
        "93": __getColor(ansi_escape_colors.get("brightColors"), "yellow", "#e79881"),
        "94": __getColor(ansi_escape_colors.get("brightColors"), "blue", "#709ad2"),
        "95": __getColor(ansi_escape_colors.get("brightColors"), "magenta", "#c58cec"),
        "96": __getColor(ansi_escape_colors.get("brightColors"), "cyan", "#70b8ca"),
        "97": __getColor(ansi_escape_colors.get("brightColors"), "white", "#f2f4f5"),
    }

    ANSI_ESCAPE_MAP_BG_COLOR = {
        # normal color mode
        "40": __getColor(ansi_escape_colors.get("normalColors"), "black", "#232526"),
        "41": __getColor(ansi_escape_colors.get("normalColors"), "red", "#df5b61"),
        "42": __getColor(ansi_escape_colors.get("normalColors"), "green", "#78b892"),
        "43": __getColor(ansi_escape_colors.get("normalColors"), "yellow", "#de8f78"),
        "44": __getColor(ansi_escape_colors.get("normalColors"), "blue", "#6791c9"),
        "45": __getColor(ansi_escape_colors.get("normalColors"), "magenta", "#bc83e3"),
        "46": __getColor(ansi_escape_colors.get("normalColors"), "cyan", "#67afc1"),
        "47": __getColor(ansi_escape_colors.get("normalColors"), "white", "#e4e6e7"),
        "49": __getColor(ansi_escape_colors.get("defaultColors"), "bg", "#101415"),
        # bright color mode
        "100": __getColor(ansi_escape_colors.get("brightColors"), "black", "#2c2e2f"),
        "101": __getColor(ansi_escape_colors.get("brightColors"), "red", "#e8646a"),
        "102": __getColor(ansi_escape_colors.get("brightColors"), "green", "#81c19b"),
        "103": __getColor(ansi_escape_colors.get("brightColors"), "yellow", "#e79881"),
        "104": __getColor(ansi_escape_colors.get("brightColors"), "blue", "#709ad2"),
        "105": __getColor(ansi_escape_colors.get("brightColors"), "magenta", "#c58cec"),
        "106": __getColor(ansi_escape_colors.get("brightColors"), "cyan", "#70b8ca"),
        "107": __getColor(ansi_escape_colors.get("brightColors"), "white", "#f2f4f5"),
    }

    @classmethod
    def convert(cls, escapeCode) -> ansiEscape:
        txtColor = cls.ANSI_ESCAPE_MAP_TXT_COLOR.get(escapeCode)
        if txtColor:
            return ansiEscape(data=txtColor, oper="txtColor")

        bgColor = cls.ANSI_ESCAPE_MAP_BG_COLOR.get(escapeCode)
        if bgColor:
            return ansiEscape(data=bgColor, oper="bgColor")

        return None
