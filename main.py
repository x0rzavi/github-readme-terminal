import gifos

FONT_FILE_LOGO = "./fonts/vtks-blocketo.regular.ttf"
# FONT_FILE_BITMAP = "./fonts/ter-u14n.pil"
FONT_FILE_BITMAP = "./fonts/gohufont-uni-14.pil"
FONT_FILE_TRUETYPE = "./fonts/IosevkaTermNerdFont-Bold.ttf"


def main():
    t = gifos.Terminal(640, 480, 15, 15, FONT_FILE_BITMAP, 15)
    t.set_fps(15)

    t.gen_text("", 1, count=20)
    t.toggle_show_cursor(False)
    t.gen_text("GIF_OS Modular BIOS v1.0.11", 1)
    t.gen_text("Copyright (C) 2023, \x1b[91mX0rzAvi Softwares Inc.\x1b[0m", 2)
    t.gen_text("\x1b[94mGitHub Profile ReadMe Terminal, Rev 1011\x1b[0m", 4)
    t.gen_text("Krypton(tm) GIFCPU - 250Hz", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to cancel Memory Test",
        t.num_rows,
    )
    for i in range(0, 65653, 7168):  # 64K Memory
        t.delete_row(7)
        if i < 30000:
            t.gen_text(
                f"Memory Test: {i}", 7, count=2, contin=True
            )  # slow down upto a point
        else:
            t.gen_text(f"Memory Test: {i}", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64KB OK", 7, count=10, contin=True)
    t.gen_text("", 11, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("\x1b[96m", 1, count=0, contin=True)  # buffer to be removed
    t.set_font(FONT_FILE_LOGO, 66)
    # t.toggle_show_cursor(True)
    os_logo_text = "GIF OS"
    mid_row = (t.num_rows + 1) // 2
    mid_col = (t.num_cols - len(os_logo_text) + 1) // 2
    effect_lines = gifos.effects.text_scramble_effect_lines(
        os_logo_text, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(mid_row + 1)
        t.gen_text(effect_lines[i], mid_row + 1, mid_col + 1)

    t.set_font(FONT_FILE_BITMAP, 15)
    t.clear_frame()
    t.clone_frame(5)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mGIF OS v1.0.11 (tty1)\x1b[0m", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("x0rzavi", 3, contin=True)
    t.gen_text("", 4, count=5)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("*********", 4, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text("Last login: Sun Dec  13 22:55:39 on tty1", 6)

    t.gen_prompt(7, count=5)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)  # simulate syntax highlighting
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=3, contin=True)

    ignore_repos = ["archiso-zfs", "archiso-zfs-archive"]
    git_user_details = gifos.utils.fetch_github_stats("x0rzavi", ignore_repos)
    user_age = gifos.utils.calc_age(26, 7, 2002)
    t.clear_frame()
    top_languages = [lang[0] for lang in git_user_details.languages_sorted]
    user_details_lines = f"""
    \x1b[30;104mx0rzavi@GitHub\x1b[0m
    --------------
    \x1b[96mOS:     \x1b[93mArch/Gentoo Linux, Windows 11, Android 13
    \x1b[96mHost:   \x1b[93mNetaji Subhash Engineering College \x1b[94m#NSEC
    \x1b[96mKernel: \x1b[93mComputer Science & Engineering \x1b[94m#CSE
    \x1b[96mUptime: \x1b[93m{user_age.years} years, {user_age.months} months, {user_age.days} days
    \x1b[96mIDE:    \x1b[93mneovim, VSCode

    \x1b[30;104mContact:\x1b[0m
    --------------
    \x1b[96mEmail:  \x1b[93mx0rzavi@gmail.com
    \x1b[96mLinkedIn: \x1b[93mavishek-sen-x0rzavi

    \x1b[30;104mGitHub Stats:\x1b[0m
    --------------
    \x1b[96mUser Rating: \x1b[93m{git_user_details.user_rank.level}
    \x1b[96mTotal Stars Earned: \x1b[93m{git_user_details.total_stargazers}
    \x1b[96mTotal Commits (2023): \x1b[93m{git_user_details.total_commits_last_year}
    \x1b[96mTotal PRs: \x1b[93m{git_user_details.total_pull_requests_made}\x1b[0m | \x1b[96mMerged PR%: \x1b[93m{git_user_details.pull_requests_merge_percentage}
    \x1b[96mTotal Contributions: \x1b[93m{git_user_details.total_repo_contributions}
    \x1b[96mTop Languages: \x1b[93m{', '.join(top_languages[:5])}\x1b[0m
    """
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(10)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u x0rzavi", 1, contin=True)

    # t.pasteImage("./temp/x0rzavi.jpg", 3, 5, sizeMulti=0.5)
    t.gen_text(user_details_lines, 2, contin=True)
    t.gen_prompt(t.curr_row)
    t.gen_text("", t.curr_row, count=120, contin=True)

    t.gen_gif()
    # image = gifos.utils.upload_imgbb("output.gif", 129600)  # 1.5 days expiration
    # print(f"Image URL: {image.url}\nDeletion URL: {image.delete_url}")


if __name__ == "__main__":
    main()
