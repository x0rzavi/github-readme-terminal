import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def load_toml(file_name: str) -> dict:
    def_config_file = (
        Path(__file__).parents[1] / "config" / file_name
    )  # default config path
    user_config_file = Path.home() / ".config" / "gifos" / file_name  # user config path

    with def_config_file.open(mode="rb") as def_fp:
        config = tomllib.load(def_fp)
    if user_config_file.exists():
        with user_config_file.open(mode="rb") as user_fp:
            user_config = tomllib.load(user_fp)
            config.update(user_config)  # override with user config
            return config
    else:
        print(f"INFO: Default config_file: {file_name} loaded")
    for section in config:
        for key in config[section]:
            env_var_name = f"GIFOS_{section.upper()}_{key.upper()}"
            env_var_value = os.getenv(env_var_name)
            if env_var_value is not None:
                config[section][key] = env_var_value
                print(f"INFO: Config updated from environment variable: {env_var_name}")
    return config


gifos = load_toml("gifos.toml")
ansi_escape_colors = load_toml("ansi_escape_colors.toml")

__all__ = ["gifos", "ansi_escape_colors"]
