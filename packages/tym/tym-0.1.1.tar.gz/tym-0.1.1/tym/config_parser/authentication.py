from configparser import ConfigParser
from tym.models import AuthenticationError


def get_email(config: ConfigParser) -> str:
    if "user" not in config:
        raise AuthenticationError({"detail": "User section not found in config."})
    user_section = config["user"]
    if "email" not in user_section:
        raise AuthenticationError({"detail": "User email not found in config."})
    return user_section["email"]


def get_refresh_token(config: ConfigParser) -> str:
    if "user" not in config:
        raise AuthenticationError({"detail": "User section not found in config."})
    user_section = config["user"]
    if "refresh_token" not in user_section:
        raise AuthenticationError({"detail": "Refresh token not found in config."})
    return user_section["refresh_token"]


def clear_auth_config(config: ConfigParser):
    # Mainly used for logging out
    if "user" in config:
        user_section = config["user"]
        if "refresh_token" in user_section:
            del user_section["refresh_token"]
    else:
        config["user"] = {}


def set_auth_config(config: ConfigParser, email: str, refresh_token: str):
    if "user" in config:
        config["user"]["email"] = email
        config["user"]["refresh_token"] = refresh_token
    else:
        config["user"] = {
            "email": email,
            "refresh_token": refresh_token,
        }
