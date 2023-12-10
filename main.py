from gifos.gifos import Terminal
from gifos.modules import helpers
from gifos.modules import textEffects

# from dotenv import load_dotenv
from PIL import ImageFont

# import os

# load_dotenv()

# fontFileTruetype = "./fonts/vtks-blocketo.regular.ttf"
# fontFileTruetype = "./fonts/orange-kid.regular.otf"
fontFileTruetype = "./fonts/IosevkaNerdFont-Medium.ttf"
fontFileBitmap = "./fonts/cherry-13-r.pil"

fontTruetype = ImageFont.truetype(fontFileTruetype, size=35)  # truetype font
fontBitmap = ImageFont.load(fontFileBitmap)  # bitmap monospaced font


def main():
    ## TEST BED
    t = Terminal(640, 480, 15, 15, fontTruetype)
    # t.toggleBlinkCursor(True)
    #     t.fps = 15
    #     t.toggleShowCursor(False)
    #     t.genText("", 1, 1, 5, False)
    #     t.genText("Starting GIF OS ", 1, 1, 5, False)
    #     t.genTypingText(".....", 1, 1, True)
    #     for i in range(0x0, 0x40000000, 0x7FFFFFF):
    #         if i < 0x20000000:
    #             t.cloneFrame(2)
    #         t.deleteRow(2)
    #         t.genText(f"Memory Check: {i}", 2, 1)
    #     t.cloneFrame(5)
    #     t.deleteRow(2)
    #     t.genText("Memory Check: 1048576KB OK", 2, 1, 5)
    #
    #     t.clearFrame()
    #     t.toggleShowCursor(True)
    #     t.genText("", 1, 1, 5)
    #     t.toggleShowCursor(False)
    #     t.genText("Enter username: ", 1, 1, 5)
    #     t.toggleShowCursor(True)
    #     t.genTypingText("x0rzavi", 1, 1, True)
    #     t.cloneFrame(5)
    #     t.toggleShowCursor(True)
    #     t.genText("", 2, 1, 5)
    #     t.toggleShowCursor(False)
    #     t.genText("Enter password: ", 2, 1, 5)
    #     t.toggleShowCursor(True)
    #     t.genTypingText("*********", 2, 1, True)
    #     t.genText("", 3, 1, 5)
    #     t.genText("Coded by x0rzavi :D", t.numRows, 1, 10)
    #     t.cloneFrame(2)
    #
    #     t.clearFrame()
    #     t.toggleShowCursor(True)
    #     t.genPrompt(1, 1, 1)
    #     t.genTypingText("fastfetch", 1, 1, True)
    #     lines1 = r"""       /\        x0rzavi@WIN-X0RZAVI
    #      /  \
    #     /\   \      OS: Arch Linux x86_64
    #    /      \     Kernel: Linux 5.15.133.1-microsoft-standard-WSL2
    #   /   ,,   \    Uptime: 2 hours, 42 minutes
    #  /   |  |  -\   Packages: 494 (pacman)
    # /_-''    ''-_\  Shell: zsh 5.9
    #                 CPU: AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx (8) @ 2.096MHz"""
    #     t.genMultiText(lines1, t.currRow + 1, 1, 10)
    #     t.genTypingText("ll -p", t.currRow, 1, True)
    #     lines2 = r"""total 180K
    # drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Dec  3 15:05 frames/
    # drwxr-xr-x 8 x0rzavi x0rzavi 4.0K Dec  3 10:48 .git/
    # -rw-r--r-- 1 x0rzavi x0rzavi 3.1K Dec  1 11:16 .gitignore
    # -rw-r--r-- 1 x0rzavi x0rzavi 106K Nov 17 12:10 gohufont-uni-14.bdf
    # -rw-r--r-- 1 x0rzavi x0rzavi 1.3K Nov 17 12:10 gohufont-uni-14.pbm
    # -rw-r--r-- 1 x0rzavi x0rzavi 5.1K Nov 17 12:10 gohufont-uni-14.pil
    # -rw-r--r-- 1 x0rzavi x0rzavi 1.1K Nov 17 11:51 LICENSE
    # -rw-r--r-- 1 x0rzavi x0rzavi  16K Dec  3 15:05 main.py
    # drwxr-xr-x 3 x0rzavi x0rzavi 4.0K Dec  3 15:04 .mypy_cache/
    # -rw-r--r-- 1 x0rzavi x0rzavi  13K Nov 24 10:15 temp.py
    # drwxr-xr-x 5 x0rzavi x0rzavi 4.0K Nov 17 12:05 venv/
    # drwxr-xr-x 2 x0rzavi x0rzavi 4.0K Dec  1 10:24 .vscode/"""
    #     t.genMultiText(lines2, t.currRow + 1, 1, 10)
    #     t.genTypingText("cat rc.conf", t.currRow, 1, True)
    #     lines3 = r"""set preview_images true
    # set preview_images_method ueberzug"""
    #     t.genMultiText(lines3, t.currRow + 1, 1, 10)

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
    # t.genMultiText(lines10, 11, 1, 1)
    # t.genMultiText(lines10, 21, 1, 1)
    # t.genMultiText(lines10, 25, 1, 1)
    # t.genMultiText(lines2, 25, 1, 5, True)
    # t.genMultiText(lines3, 21, 1, 1, False)
    # t.genMultiText(lines3, 3, 1, 1, False)

    # ignoreRepos = ["archiso-zfs", "archiso-zfs-archive"]
    # userDetails = helpers.calcUserStats("x0rzavi", ignoreRepos, True)
    # print(userDetails)
    # t.genText(userDetails["accountName"] + "'s Github Stats", 1, 1)
    # t.genText(
    #     "Total Commits (Last Year): " + str(userDetails["totalCommitsLastYear"]), 2, 1
    # )

    t.setFont(fontBitmap)
    t.setFps(10)
    lines = textEffects.textDecodeEffectLines("GOODBYE WORLD!", 3)
    t.toggleShowCursor(False)
    for line in lines:
        t.deleteRow(5)
        t.genText(line, 5, 1)
    t.genGif()


if __name__ == "__main__":
    main()
