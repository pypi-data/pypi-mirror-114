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

import praw
from time import sleep
from .misc import checkMessage, getCredentials

def tadr(Log, messageIDs, Static):
    
    
    Log.new("Initialising Reddit instance...")
    reddit = praw.Reddit(
        user_agent=Static.OS+":tor-auto-done-replier:v"+Static.VERSION+" (by /u/MurdoMaclachlan)",
        **getCredentials(Log, Static)
    )
    
    # Main program loop
    while True:
        
        # Fetch messages
        Log.new("Checking messages...")
        for message in reddit.inbox.comment_replies(limit=Static.LIMIT):
            
            # Main check, replying to message if necessary
            # The one second delay should ensure only 1 reply is ever needed
            if checkMessage(Log, message, messageIDs, Static):
                Log.new(f"Replying to message at: https://www.reddit.com{message.context}")
                if Static.VERBOSE: Log.Notify.Notification.new(f"Replying to message at: {message.id}").show()
                sleep(1)
                message.reply(Static.REPLY)
        
        # Extra logs / functions depending on settings
        if Static.DEBUG: Log.new(f"Messages checked so far: \n{messageIDs}")
        if not Log.failed and Static.LOG_UPDATES: Log.new("Updating log..."); Log.update(Static)
        Log.new(f"Finished checking messages, waiting {Static.SLEEP} seconds.")
        
        sleep(Static.SLEEP)
