from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def load_toml(file_name: str) -> dict:
    def_config_file = (
        Path(__file__).parents[2] / "config" / file_name
    )  # default config path
    user_config_file = Path.home() / ".config" / "gifos" / file_name  # user config path

    with def_config_file.open(mode="rb") as def_fp:
        def_config = tomllib.load(def_fp)
    if user_config_file.exists():
        with user_config_file.open(mode="rb") as user_fp:
            user_config = tomllib.load(user_fp)
            return {**def_config, **user_config}  # override with user config
    print(f"INFO: default config_file {file_name} loaded")
    return def_config


gifos = load_toml("gifos.toml")
ansi_escape_colors = load_toml("ansi_escape_colors.toml")

__all__ = ["gifos", "ansi_escape_colors"]
