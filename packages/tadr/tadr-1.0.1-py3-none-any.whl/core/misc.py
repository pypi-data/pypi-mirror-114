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
    
    Contact me at murdo@maclachlans.org.uk
"""

from configparser import ConfigParser
from datetime import datetime
from typing import Dict, List

def checkMessage(Log: object, message: object, messageIDs: List, Static: object) -> bool:
    
    # Avoid checking messages from before program start, or that have already been checked
    if message.created_utc < Static.START_TIME or message.id in messageIDs:
        return False
    
    messageIDs.append(message.id)
    
    if message.body.split(Static.SPLITTER)[0] in Static.MESSAGES and message.author.name in Static.AUTHORS:
        
        # Declaring these variables saves on API requests and speeds up program a lot.
        # They'll be deleted later on to ensure memory is saved, because I don't know
        # whether or not Python does that for you.
        parent = message.parent()
        parentBody = parent.body.casefold()
        
        # Haven't tried re-replying; try.
        if parentBody == "done":
            del parent, parentBody
            return True
        
        # Have tried re-replying; there's a problem.
        elif parentBody == Static.REPLY:
            Log.Notify.Notification.new(f"Problematic post found.").show()
            Log.new(Log.warning(f"Problematic post at: {parent.url}"))
            del parent, parentBody
            return False

# Use configparser magic to get the credentials from praw.ini
def getCredentials(Log: object, Static: object) -> Dict:
    
    # Read config section titled "adr" and return details
    try:
        credentials = ConfigParser()
        credentials.read(f"{Static.PATHS['config']}/praw.ini")
        return dict(credentials["tadr"])
    
    # If praw.ini is missing, warn the user
    except (FileNotFoundError, KeyError):
        Log.new(Log.warning("praw.ini not found; please set up praw.ini and then re-run TADR. See README.md for instructions."))
        exit()

# Returns current time in human readable format
def getTime(timeToFind: float) -> str:
    return datetime.fromtimestamp(timeToFind).strftime("%Y-%m-%d %H:%M:%S")
