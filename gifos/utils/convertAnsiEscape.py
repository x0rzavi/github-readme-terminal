from .schemas.ansiEscape import ansiEscape


class convertAnsiEscape:
    ANSI_ESCAPE_MAP_FG_COLOR = {
        # normal color mode
        "30": "#232526",  # black
        "31": "#df5b61",  # red
        "32": "#78b892",  # green
        "33": "#de8f78",  # yellow
        "34": "#6791c9",  # blue
        "35": "#bc83e3",  # magenta
        "36": "#67afc1",  # cyan
        "37": "#e4e6e7",  # white
        "39": "#F2F4F5",  # default
        # bright color mode
        "90": "#2c2e2f",  # bright black
        "91": "#e8646a",  # bright red
        "92": "#81c19b",  # bright green
        "93": "#e79881",  # bright yellow
        "94": "#709ad2",  # bright blue
        "95": "#c58cec",  # bright magenta
        "96": "#70b8ca",  # bright cyan
        "97": "#f2f4f5",  # bright white
    }

    ANSI_ESCAPE_MAP_BG_COLOR = {
        # normal color mode
        "40": "#232526",  # black
        "41": "#df5b61",  # red
        "42": "#78b892",  # green
        "43": "#de8f78",  # yellow
        "44": "#6791c9",  # blue
        "45": "#bc83e3",  # magenta
        "46": "#67afc1",  # cyan
        "47": "#e4e6e7",  # white
        "49": "#101415",  # default
        # bright color mode
        "100": "#2c2e2f",  # bright black
        "101": "#e8646a",  # bright red
        "102": "#81c19b",  # bright green
        "103": "#e79881",  # bright yellow
        "104": "#709ad2",  # bright blue
        "105": "#c58cec",  # bright magenta
        "106": "#70b8ca",  # bright cyan
        "107": "#f2f4f5",  # bright white
    }

    @classmethod
    def convert(cls, escapeCode) -> ansiEscape:
        txtColor = cls.ANSI_ESCAPE_MAP_FG_COLOR.get(escapeCode)
        if txtColor:
            return ansiEscape(data=txtColor, op="txtColor")

        bgColor = cls.ANSI_ESCAPE_MAP_BG_COLOR.get(escapeCode)
        if bgColor:
            return ansiEscape(data=bgColor, op="bgColor")

        return None
