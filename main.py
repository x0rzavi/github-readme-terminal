from gifos.gifos import Terminal
from gifos import utils
from gifos import effects


fontFileTruetype = "./fonts/vtks-blocketo.regular.ttf"
# fontFileBitmap = "./fonts/ter-u14n.pil"
fontFileBitmap = "./fonts/gohufont-uni-14.pil"


def main():
    t = Terminal(640, 480, 15, 15, fontFileBitmap)
    t.setFps(15)

    t.genText("", 1, count=20)
    t.toggleShowCursor(False)
    t.genText("GIF_OS Modular BIOS v1.0.11", 1)
    t.genText("Copyright (C) 2023, \x1b[91mX0rzAvi Softwares Inc.\x1b[0m", 2)
    t.genText("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.genText("Krypton(tm) GIFCPU - 250Hz", 6)
    t.genText(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.numRows,
    )
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
    t.genText("\x1b[96m", 1, count=0, contin=True)  # buffer to be removed
    t.setFont(fontFileTruetype, 66)
    # t.toggleShowCursor(True)
    osLogoText = "GIF OS"
    midRow = (t.numRows + 1) // 2
    midCol = (t.numCols - len(osLogoText) + 1) // 2
    effectLines = effects.textScrambleEffectLines(osLogoText, 3, includeSpecial=False)
    for i in range(len(effectLines)):
        if i == len(effectLines) // 2:
            t.genText(
                "\x1b[93m", midRow + 1, count=0, contin=True
            )  # buffer to be removed
        t.deleteRow(midRow + 1)
        t.genText(effectLines[i], midRow + 1, midCol + 1)

    t.setFont(fontFileBitmap)
    t.clearFrame()
    t.cloneFrame(5)
    t.toggleShowCursor(False)
    t.genText("\x1b[93mGIF OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.genText("login: ", 3, count=5)
    t.toggleShowCursor(True)
    t.genTypingText("x0rzavi", 3, contin=True)
    t.genText("", 4, count=5)
    t.toggleShowCursor(False)
    t.genText("password: ", 4, count=5)
    t.toggleShowCursor(True)
    t.genTypingText("*********", 4, contin=True)
    t.toggleShowCursor(False)
    t.genText("Last login: Sun Dec  13 22:55:39 on tty1", 6)
    t.genPrompt(7, count=5)
    t.toggleShowCursor(True)
    t.genTypingText("clear", 7, contin=True)

    ignoreRepos = ["archiso-zfs", "archiso-zfs-archive"]
    gitUserDetails = utils.fetchGithubStats("x0rzavi", ignoreRepos, True)
    userAge = utils.calcAge(26, 7, 2002)
    t.clearFrame()
    topLanguages = [lang[0] for lang in gitUserDetails.languagesSorted]
    userDetailsLines = rf"""
    \x1b[96;100mx0rzavi@GitHub\x1b[0m
    -------------------
    \x1b[94mOS:     \x1b[93mArch/Gentoo Linux, Windows 11, Android 13
    \x1b[94mHost:   \x1b[93mNetaji Subhash Engineering College #NSEC
    \x1b[94mKernel: \x1b[93mComputer Science & Engineering #CSE
    \x1b[94mUptime: \x1b[93m{userAge.years} years, {userAge.months} months, {userAge.days} days
    \x1b[94mIDE:    \x1b[93mneovim, VSCode

    \x1b[96;100mContact:\x1b[0m
    -------------------
    \x1b[94mEmail:  \x1b[93mx0rzavi@gmail.com
    \x1b[94mLinkedIn: \x1b[93mavishek-sen-x0rzavi

    \x1b[96;100mGitHub Stats:\x1b[0m
    -------------------
    \x1b[94mUser Rating: \x1b[93m{gitUserDetails.userRank.level}
    \x1b[94mTotal Stars Earned: \x1b[93m{gitUserDetails.totalStargazers}
    \x1b[94mTotal Commits (2023): \x1b[93m{gitUserDetails.totalCommitsLastYear}
    \x1b[94mTotal PRs: \x1b[93m{gitUserDetails.totalPullRequestsMade}\x1b[0m | \x1b[94mMerged PR%: \x1b[93m{gitUserDetails.pullRequestsMergePercentage}
    \x1b[94mTotal Contributions: \x1b[93m{gitUserDetails.totalRepoContributions}
    \x1b[94mTop Languages: \x1b[93m{', '.join(topLanguages[:5])}\x1b[0m
    """
    t.genPrompt(1)
    t.cloneFrame(10)
    t.toggleShowCursor(True)
    t.genTypingText("statsfetch -u x0rzavi", 1, contin=True)
    t.genText(userDetailsLines, 2)
    t.genPrompt(t.currRow)
    t.genText("", t.currRow, count=100, contin=True)

    t.genGif()
    # image = utils.uploadImgBB("output.gif", 129600)  # 1.5 days expiration
    # print(f"Image URL: {image.url}\nDeletion URL: {image.deleteUrl}")


if __name__ == "__main__":
    main()
