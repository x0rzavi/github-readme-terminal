try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from pathlib import Path


def loadtoml(filename: str) -> dict:
    configfile = Path("./config") / filename
    if configfile.exists():
        with configfile.open(mode="rb") as fp:
            return tomllib.load(fp)
    else:
        print(f"INFO: configfile {filename} does not exist")
        return {}


gifos = loadtoml("gifos.toml")
ansi_escape_colors = loadtoml("ansi_escape_colors.toml")

__all__ = ["gifos", "ansi_escape_colors"]
