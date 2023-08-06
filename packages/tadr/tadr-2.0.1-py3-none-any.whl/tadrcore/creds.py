"""
    Copyright (C) 2021-present, Murdo B. Maclachlan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

    Contact me at murdomaclachlan@duck.com
"""

from configparser import ConfigParser
from typing import Dict, NoReturn
from .globals import Globals
from .logger import Log

global Globals, Log


def add_refresh_token(creds: Dict, refresh_token: str) -> NoReturn:
    """Appends a given Reddit refresh token to praw.ini.

    Arguments:
    - refresh_token (string)

    No return value.
    """
    creds["refresh_token"] = refresh_token
    dump_credentials(creds)


def create_credentials() -> bool:
    """Creates a new ini file based on user input.

    No arguments.

    Returns: boolean success status.
    """
    Log.new(
        "praw.ini missing, incomplete or incorrect. It will need to be created.",
        "INFO"
    )
    creds = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": input("Please input your username:  "),
        "redirect_uri": "http://localhost:8080/users/auth/reddit/callback",
    }
    try:
        return dump_credentials(creds)
    except FileNotFoundError:
        return False


def dump_credentials(creds: Dict) -> NoReturn:
    """Outputs updated Reddit credentials to praw.ini.

    Arguments:
    - creds (dictionary)

    Returns: boolean success status.
    """
    Parser = ConfigParser()
    Parser["tcf"] = creds
    with open(f"{Globals.PATHS['config']}/praw.ini", "w+") as dump_file:
        Parser.write(dump_file)
    return True


def get_credentials() -> Dict:
    """Retrieves Reddit credentials from praw.ini.

    No arguments.

    Returns: dictionary containing credentials.
    """
    try:
        Parser = ConfigParser()
        Parser.read(f"{Globals.PATHS['config']}/praw.ini")
        return dict(Parser["tcf"])
    except FileNotFoundError:
        if create_credentials():
            return get_credentials()
        else:
            Log.new(
                "Could not create praw.ini! Encountered an error during ini creation.",
                "FATAL"
            )