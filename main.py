from PIL import ImageFont
from gifos.gifos import Terminal
from gifos import utils
from gifos import effects


fontFileTruetype = "./fonts/vtks-blocketo.regular.ttf"
# fontFileTruetype = "./fonts/SpaceMonoNerdFontMono-Bold.ttf"
fontFileBitmap = "./fonts/ter-u14n.pil"
# fontFileBitmap = "./fonts/cherry-13-r.pil"

fontTruetype = ImageFont.truetype(fontFileTruetype, size=66)  # truetype font
fontBitmap = ImageFont.load(fontFileBitmap)  # bitmap monospaced font


def main():
    t = Terminal(640, 480, 15, 15, fontBitmap)
    t.setFps(15)

    t.genText("", 1, count=20)
    t.toggleShowCursor(False)
    t.genText("GIF_OS Modular BIOS v1.0.11", 1)
    t.genText("Copyright (C) 2023, X0rzAvi Softwares Inc.", 2)
    t.toggleHighlight()
    t.genText("GitHub Profile ReadMe Terminal, Rev 1011", 4)
    t.toggleHighlight()
    t.genText("Krypton(tm) GIFCPU - 250Hz", 6)
    t.genText("Press DEL to enter SETUP, ESC to cancel Memory Test", t.numRows)
    for i in range(0, 65653, 7168):  # 64K Memory
        t.deleteRow(7)
        if i < 30000:
            t.genText(
                f"Memory Test: {i}", 7, count=2, contin=True
            )  # slow down upto a point
        else:
            t.genText(f"Memory Test: {i}", 7, contin=True)
    t.deleteRow(7)
    t.genText("Memory Test: 64KB OK", 7, count=10, contin=True)
    t.genText("", 11, count=10, contin=True)

    t.clearFrame()
    t.genText("Initiating Boot Sequence ", 1, contin=True)
    t.genTypingText(".....", 1, contin=True)
    t.setFont(fontTruetype)
    # t.toggleShowCursor(True)
    osLogoText = "GIF OS"
    midRow = (t.numRows + 1) // 2
    midCol = (t.numCols - len(osLogoText) + 1) // 2
    effectLines = effects.textScrambleEffectLines(
        osLogoText, 3, includeSpecial=False
    )
    t.toggleHighlight()
    for effectLine in effectLines:
        t.deleteRow(midRow)
        t.genText(effectLine, midRow, midCol + 1)
    t.toggleHighlight()

    t.setFont(fontBitmap)
    t.setTxtColor()
    t.clearFrame()
    t.cloneFrame(5)
    t.toggleShowCursor(False)
    t.toggleHighlight()
    t.genText("GIF OS v1.0.11 (tty1)", 1, count=5)
    t.toggleHighlight()
    t.genText("login: ", 3, count=5)
    t.toggleShowCursor(True)
    t.genTypingText("x0rzavi", 3, contin=True)
    t.genText("", 4, count=5)
    t.toggleShowCursor(False)
    t.genText("password: ", 4, count=5)
    t.toggleShowCursor(True)
    t.genTypingText("*********", 4, contin=True)
    t.toggleShowCursor(False)
    t.genText("Last login: Sun Dec  12 00:18:39 on tty1", 6)
    t.toggleHighlight()
    t.genPrompt(7, count=5)
    t.toggleHighlight()
    t.toggleShowCursor(True)
    t.genTypingText("clear", 7, contin=True)

    ignoreRepos = ["archiso-zfs", "archiso-zfs-archive"]
    gitUserDetails = utils.calcUserStats("x0rzavi", ignoreRepos, True)
    userAge = utils.calcAge(26, 7, 2002)
    t.clearFrame()
    topLanguages = [lang[0] for lang in gitUserDetails["languagesSorted"]]
    userDetailsLines = rf"""
    x0rzavi@GitHub
    -------------------
    OS:     Arch/Gentoo Linux, Windows 11, Android 14
    Host:   Netaji Subhash Engineering College #NSEC
    Kernel: Computer Science & Engineering #CSE
    Uptime: {userAge[0]} years, {userAge[1]} months, {userAge[2]} days
    IDE:    neovim, VSCode

    Contact:
    -------------------
    Email:  x0rzavi@gmail.com
    LinkedIn: avishek-sen-x0rzavi

    GitHub Stats:
    -------------------
    User Rating: {gitUserDetails['userRank']['level']}
    Total Stars Earned: {gitUserDetails['totalStargazers']}
    Total Commits: {gitUserDetails['totalCommitsAllTime']}
    Total PRs: {gitUserDetails['totalPullRequestsMade']} | Merged PR%: {gitUserDetails['pullRequestsMergePercentage']}
    Total Contributions: {gitUserDetails['totalRepoContributions']}
    Top Languages: {', '.join(topLanguages[:5])}
    """
    t.toggleHighlight()
    t.genPrompt(1)
    t.toggleHighlight()
    t.cloneFrame(10)
    t.toggleShowCursor(True)
    t.genTypingText("statsfetch -u x0rzavi", 1, contin=True)
    t.genMultiText(userDetailsLines, 2, prompt=False)
    t.toggleHighlight()
    t.genPrompt(t.currRow)
    t.toggleHighlight()
    t.genText("", t.currRow, count=100, contin=True)

    t.genGif()
    utils.uploadImage("output.gif", 129600) # 1.5 days expiration


if __name__ == "__main__":
    main()
