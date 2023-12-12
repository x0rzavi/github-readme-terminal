class convertAnsiEscape:
    ANSI_ESCAPE_MAP_FG_COLOR = {
        # normal color mode
        "30": "#232526",
        "31": "#df5b61",
        "32": "#78b892",
        "33": "#de8f78",
        "34": "#6791c9",
        "35": "#bc83e3",
        "36": "#67afc1",
        "37": "#e4e6e7",
        "39": "#F2F4F5",
        # bright color mode
        "90": "#2c2e2f",
        "91": "#e8646a",
        "92": "#81c19b",
        "93": "#e79881",
        "94": "#709ad2",
        "95": "#c58cec",
        "96": "#70b8ca",
        "97": "#f2f4f5",
    }

    ANSI_ESCAPE_MAP_BG_COLOR = {
        # normal color mode
        "40": "#232526",
        "41": "#df5b61",
        "42": "#78b892",
        "43": "#de8f78",
        "44": "#6791c9",
        "45": "#bc83e3",
        "46": "#67afc1",
        "47": "#e4e6e7",
        "49": "#F2F4F5",
        # bright color mode
        "100": "#2c2e2f",
        "101": "#e8646a",
        "102": "#81c19b",
        "103": "#e79881",
        "104": "#709ad2",
        "105": "#c58cec",
        "106": "#70b8ca",
        "107": "#f2f4f5",
    }

    @classmethod
    def get(cls, escapeCode) -> dict:
        fg_color = cls.ANSI_ESCAPE_MAP_FG_COLOR.get(escapeCode)
        if fg_color:
            return {"color": fg_color, "op": "txtColor"}

        bg_color = cls.ANSI_ESCAPE_MAP_BG_COLOR.get(escapeCode)
        if bg_color:
            return {"color": bg_color, "op": "bgColor"}

        return None
