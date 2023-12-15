from gifos.gifos import Terminal
from gifos import utils
from gifos import effects


fontFileLogo = "./fonts/vtks-blocketo.regular.ttf"
# fontFileBitmap = "./fonts/ter-u14n.pil"
fontFileBitmap = "./fonts/gohufont-uni-14.pil"
fontFileTruetype = "./fonts/IosevkaTermNerdFont-Bold.ttf"


def main():
    t = Terminal(640, 480, 15, 15, fontFileBitmap, 15)
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
    t.setFont(fontFileLogo, 66)
    # t.toggleShowCursor(True)
    osLogoText = "GIF OS"
    midRow = (t.numRows + 1) // 2
    midCol = (t.numCols - len(osLogoText) + 1) // 2
    effectLines = effects.textScrambleEffectLines(osLogoText, 3, includeSpecial=False)
    for i in range(len(effectLines)):
        t.deleteRow(midRow + 1)
        t.genText(effectLines[i], midRow + 1, midCol + 1)

    t.setFont(fontFileBitmap, 15)
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
    promptCol = t.currCol
    t.toggleShowCursor(True)
    t.genTypingText("\x1b[91mclea", 7, contin=True)
    t.deleteRow(7, promptCol)  # simulate syntax highlighting
    t.genText("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    ignoreRepos = ["archiso-zfs", "archiso-zfs-archive"]
    gitUserDetails = utils.fetchGithubStats("x0rzavi", ignoreRepos, True)
    userAge = utils.calcAge(26, 7, 2002)
    t.clearFrame()
    topLanguages = [lang[0] for lang in gitUserDetails.languagesSorted]
    userDetailsLines = f"""
    \x1b[30;104mx0rzavi@GitHub\x1b[0m
    ---------
    \x1b[96mOS:     \x1b[93mArch/Gentoo Linux, Windows 11, Android 13
    \x1b[96mHost:   \x1b[93mNetaji Subhash Engineering College \x1b[94m#NSEC
    \x1b[96mKernel: \x1b[93mComputer Science & Engineering \x1b[94m#CSE
    \x1b[96mUptime: \x1b[93m{userAge.years} years, {userAge.months} months, {userAge.days} days
    \x1b[96mIDE:    \x1b[93mneovim, VSCode

    \x1b[30;104mContact:\x1b[0m
    ----------
    \x1b[96mEmail:  \x1b[93mx0rzavi@gmail.com
    \x1b[96mLinkedIn: \x1b[93mavishek-sen-x0rzavi

    \x1b[30;104mGitHub Stats:\x1b[0m
    ----------
    \x1b[96mUser Rating: \x1b[93m{gitUserDetails.userRank.level}
    \x1b[96mTotal Stars Earned: \x1b[93m{gitUserDetails.totalStargazers}
    \x1b[96mTotal Commits (2023): \x1b[93m{gitUserDetails.totalCommitsLastYear}
    \x1b[96mTotal PRs: \x1b[93m{gitUserDetails.totalPullRequestsMade}\x1b[0m | \x1b[96mMerged PR%: \x1b[93m{gitUserDetails.pullRequestsMergePercentage}
    \x1b[96mTotal Contributions: \x1b[93m{gitUserDetails.totalRepoContributions}
    \x1b[96mTop Languages: \x1b[93m{', '.join(topLanguages[:5])}\x1b[0m
    """
    t.genPrompt(1)
    promptCol = t.currCol
    t.cloneFrame(10)
    t.toggleShowCursor(True)
    t.genTypingText("\x1b[91mfetch.s", 1, contin=True)
    t.deleteRow(1, promptCol)
    t.genText("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.genTypingText(" -u x0rzavi", 1, contin=True)

    # t.pasteImage("./temp/x0rzavi.jpg", 3, 5, sizeMulti=0.5)
    t.genText(userDetailsLines, 2, contin=True)
    t.genPrompt(t.currRow)
    t.genText("", t.currRow, count=120, contin=True)

    t.genGif()
    image = utils.uploadImgBB("output.gif", 129600)  # 1.5 days expiration
    print(f"Image URL: {image.url}\nDeletion URL: {image.deleteUrl}")


if __name__ == "__main__":
    main()
