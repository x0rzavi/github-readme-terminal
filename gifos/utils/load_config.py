from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def load_toml(file_name: str) -> dict:
    config_file = Path("config") / file_name
    if config_file.exists():
        with config_file.open(mode="rb") as fp:
            return tomllib.load(fp)
    else:
        print(f"INFO: config_file {file_name} does not exist")
        return {}


gifos = load_toml("gifos.toml")
ansi_escape_colors = load_toml("ansi_escape_colors.toml")

__all__ = ["gifos", "ansi_escape_colors"]
