<p align="center">
    <img width="640" alt="github-readme-terminal" src="https://raw.githubusercontent.com/x0rzavi/github-readme-terminal/main/docs/assets/logo.png">
    <br>
    <b>✨ Elevate your GitHub Profile ReadMe with Minimalistic Retro Terminal GIFs 🚀</b>
</p>

# 💻 GitHub ReadME Terminal 🎞️

## 📘 Description

A Python project that empowers you to create visually stunning and unique GIFs for your GitHub Profile ReadME. Unleash your creativity and make your profile stand out from the rest!

## 📸 Showcase

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://i.ibb.co/3N50TJ2/output-gif.gif">
    <source media="(prefers-color-scheme: light)" srcset="https://i.ibb.co/3N50TJ2/output-gif.gif">
    <img alt="GIFOS" src="https://i.ibb.co/3N50TJ2/output-gif.gif">
</picture>

## 🗝️ Key Features

- 👾 **Retro Vibes** – Easily simulate a retro PC booting up into a *nix terminal and then running neofetch to display various details about your GitHub activity.
- 🖼️ **Unleash Your Creativity** - Craft unique and eye-catching visuals with complete control. Your GitHub profile is your canvas, and github-readme-terminal is your paintbrush!
- 📈 **Live GitHub Stats** - Keep your profile readme up to date with your latest achievements and contributions with built-in helper functions.
- 🎨 **Choice of Color Schemes** – 10+ popular color schemes to choose from and full support for ANSI color escape sequences.
- 🛠️ **TOML-based configuration** - Provides an easy and organized way to customize your terminal simulation.

## 🎯 Motivation

- 🌈 **Customization** is at the heart of the project – no more settling for pre-defined templates. Tailor your GitHub Profile ReadME to reflect your personality.
- 🌐 Unlike other GitHub user statistic generators, this project offers a **fresh approach** to showcasing your profile information.
- 🚨 Stand out in the developer community with **visually appealing** GIFs that can potentially make a lasting impression.
- 📦 **High-level constructs** and functions for simulating various terminal operations provide unparalleled control over your ReadME aesthetic.

## ⚙️ Prerequisites

1. Python >=3.9
2. [FFmpeg](https://ffmpeg.org/download.html)
3. [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) (Optional)
4. [ImgBB API key](https://api.imgbb.com/) (Optional)

## 📦 Installation

⚙️ To install `github-readme-terminal`, you need `pip`:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --upgrade github-readme-terminal
```

## 🪧 Usage

Here is a basic demonstration:

```python
import gifos

t = gifos.Terminal(width=320, height=240, xpad=5, ypad=5)
t.gen_text(text="Hello World!", row_num=1)
t.gen_text(text="With \x1b[32mANSI\x1b[0m escape sequence support!", row_num=2)
github_stats = gifos.utils.fetch_github_stats(
    user_name="x0rzavi"
)  # needs GITHUB_TOKEN in .env or as environment variable
t.delete_row(row_num=1)
t.gen_text(text=f"GitHub Name: {github_stats.account_name}", row_num=1, contin=True)
t.gen_gif()
image = gifos.utils.upload_imgbb(
    file_name="output.gif", expiration=60
)  # needs IMGBB_API_KEY in .env or as environment variable
print(image.url)
```

For advanced usage, please refer [here](https://github.com/x0rzavi/x0rzavi)

## 🛠️ Configuration

Tunable options can be set in two locations:

1. Inside TOML files located in `~/.config/gifos/`.
2. As environment variables.

The format of TOML configuration files / environment variables are:

### 📑 gifos.toml

```toml
[general]
debug = false
cursor = "_"
show_cursor = true
blink_cursor = false
user_name = "x0rzavi" # for prompt
fps = 15
color_scheme = "rose-pine"

[files]
frame_base_name = "frame_"
frame_folder_name = "frames"
output_gif_name = "output"
```

### 📑 ansi_escape_colors.toml

```toml
[yoru]
        [yoru.default_colors]
        fg = "#edeff0"
        bg = "#0c0e0f"

        [yoru.normal_colors]
        black = "#232526"
        red = "#df5b61"
        green = "#78b892"
        yellow = "#de8f78"
        blue = "#6791c9"
        magenta = "#bc83e3"
        cyan = "#67afc1"
        white = "#e4e6e7"

        [yoru.bright_colors]
        black = "#2c2e2f"
        red = "#e8646a"
        green = "#81c19b"
        yellow = "#e79881"
        blue = "#709ad2"
        magenta = "#c58cec"
        cyan = "#70b8ca"
        white = "#f2f4f5"
```

### 📑 Environment variables

```bash
export GIFOS_GENERAL_DEBUG=true
export GIFOS_GENERAL_COLOR_SCHEME="catppuccin-mocha"
export GIFOS_CATPPUCCIN-MOCHA_DEFAULT_COLORS_FG="white"
export GIFOS_CATPPUCCIN-MOCHA_DEFAULT_COLORS_BG="black"
# Other variables are named similarly
```

Optional API keys for modules which must be present in `.env` file or declared as environment variables:

1. `GITHUB_TOKEN` - with permissions 
2. `IMGBB_API_KEY`

## 📃 Roadmap

- [ ] Add GitHub streak statistics.
- [ ] Add proper documentation.
- [ ] Properly handle exceptions.
- [ ] Add unit tests.
- [ ] Support for more ANSI escape codes.
- [ ] More in-built color schemes.
- [ ] More in-built text animations.

## 🌱 Contributing

This is an open source project licensed under MIT and we welcome contributions from the community. We appreciate all types of contributions, including bug reports, feature requests, documentation improvements, and code contributions.

## 🤝 Acknowledgments

- [liamg/liamg](https://github.com/liamg/liamg) - Inspiration.
- [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) - GitHub Stats calculation logic.
- [hchargois/gohufont](https://github.com/hchargois/gohufont) - Built-in font file.
- Creators of all the color schemes included in this project.

## ✨ Craft your masterpiece with github-readme-terminal and showcase your unique GitHub profile [here](https://github.com/x0rzavi/github-readme-terminal/discussions/categories/show-and-tell) ✨
