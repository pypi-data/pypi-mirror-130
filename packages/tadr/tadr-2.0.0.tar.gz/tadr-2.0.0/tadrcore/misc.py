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

from typing import List
from .globals import Globals
from .logger import Log

global Globals, Log


def check_message(
    message: object, messageIDs: List, Notify: object
) -> bool:
    """Check whether a given message should be replied to or not.

    :param message: The message to check
    :param messageIDs: The list of messages already replied to
    :param Notify: The desktop notification manager

    :return: Boolean success status
    """
    # Avoid checking messages from before program start, or that have already been
    # checked

    if (
        (
            message.created_utc > Globals.START_TIME
            and not message.id in messageIDs
        )
        and message.body.split(Globals.SPLITTER)[0] in Globals.MESSAGES
        and message.author.name in Globals.AUTHORS
    ):
        messageIDs.append(message.id)

        # Declaring these variables saves on API requests and speeds up program a lot.
        parent = message.parent()
        parentBody = parent.body.casefold()

        # Haven't tried re-replying; try.
        if parentBody == "done":
            return True

        # Have tried re-replying; there's a problem.
        elif parentBody == Globals.REPLY:
            Notify.Notification.new("Problematic post found.").show()
            Log.new(f"Problematic post at: {parent.url}", "INFO")
            return False
    else:
        return False