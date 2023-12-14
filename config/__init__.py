from pathlib import Path
import tomllib


def loadToml(fileName: str) -> dict:
    configFile = Path(__file__).parent / fileName
    if configFile.exists():
        with configFile.open(mode="rb") as fp:
            return tomllib.load(fp)
    else:
        print(f"INFO: configfile {fileName} does not exist")
        return {}


ansiEscapeColors = loadToml("ansiEscapeColors.toml")
gifos = loadToml("gifos.toml")

__all__ = ["ansiEscapeColors", "gifos"]
