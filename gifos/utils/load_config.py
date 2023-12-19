import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

"""This module contains a function for loading a TOML configuration file or updating configuration with environment variables."""


def load_toml(file_name: str) -> dict:
    """Load a TOML configuration file.

    This function reads a TOML configuration file and returns a dictionary containing
    the configuration values. The function first looks for the configuration file in a
    default location and loads the configuration values. If a user configuration file
    exists in the user's home directory, the function reads it and updates the
    configuration values accordingly. The function also updates the configuration values
    with any matching environment variables.

    :param file_name: The name of the configuration file to load.
    :type file_name: str
    :return: A dictionary containing the configuration values.
    :rtype: dict
    """

    def __update_config_with_env_vars(config, prefix="GIFOS"):
        for key, value in config.items():
            if isinstance(value, dict):
                __update_config_with_env_vars(value, f"{prefix}_{key.upper()}")
            else:
                env_var_name = f"{prefix}_{key.upper()}"
                env_var_value = os.getenv(env_var_name)
                if env_var_value is not None:
                    if env_var_value.lower() in ['true', 'false']:  # check if the env var is a boolean
                        env_var_value = env_var_value.lower() == 'true' # convert to boolean
                    config[key] = env_var_value
                    print(
                        f"INFO: Config updated from environment variable: {env_var_name}={env_var_value}"
                    )

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
    __update_config_with_env_vars(config)
    return config


gifos_settings = load_toml("gifos_settings.toml")
ansi_escape_colors = load_toml("ansi_escape_colors.toml")

__all__ = ["gifos_settings", "ansi_escape_colors"]
