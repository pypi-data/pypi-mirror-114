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

from colored import fg, attr
from os import environ, mkdir
from os.path import expanduser, isdir
from sys import platform
from time import time
from typing import List, NoReturn
from .misc import getTime

global VERSION
VERSION = "1.0.1"

# For console logging
class Log:
    
    def __init__(self, Notify: object) -> NoReturn:
        self.__log = []
        self.ConsoleColours = self.Colours(130, 0)
        self.failed = False
        self.Notify = Notify
        self.Notify.init("Auto Done Replier")
        
    class Colours:
            
        def __init__(self: object, warning: int, reset: int) -> NoReturn:
            self.RESET = attr(reset)
            self.WARNING = fg(warning)
    
    # Log to console, all that jazz
    def new(self, message: str) -> NoReturn:
        message = f"{getTime(time())} - {message}"
        self.__log.append(message)
        print(message)
    
    # Tries to update log.txt file; if it can't find the data directory,
    # it'll make it. On any unexpected exception, it'll disable future
    # log updates and spit the error to the console.
    def update(self, Static: object) -> NoReturn:
        if not self.failed:
            try:
                if not isdir(Static.PATHS["data"]):
                    self.new("data directory not found, it will be created.")
                    mkdir(Static.PATHS["data"])
                with open(f"{Static.PATHS['data']}/log.txt", "a") as file:
                    for i in self.__log:
                        file.write(f"{i}\n")
            except Exception as e:
                self.new(f"Failed to update log with error:\n{e}")
                self.failed = True
    
    # Returns a string that will appear coloured when printed to the console
    def warning(self, message: str) -> str:
        return self.ConsoleColours.WARNING + "WARNING: " + message + self.ConsoleColours.RESET

# Contains all static vars
class Static:
    
    def __init__(self, Log) -> NoReturn:
        self.AUTHORS = ["transcribersofreddit"]
        self.DEBUG = False
        self.LIMIT = 10
        self.LOG_UPDATES = False
        self.MESSAGES = ["Sorry; I can't find your transcript post on the link"]
        self.OS = platform
        self.PATHS = self.definePaths(expanduser("~"), self.OS, Log)
        self.REPLY = "done -- this was an automated action; please contact me with any questions."
        self.SLEEP = 10
        self.SPLITTER = "."
        self.START_TIME = time()
        self.VERBOSE = True
        self.VERSION = VERSION
    
    # Defines save paths for config and data based on the user's OS    
    def definePaths(self, home: str, os: str, Log: object) -> List:
        
        # Gets first 3 characters of OS
        os = ''.join(list(os)[:3])
        
        if os in ["dar", "lin", "win"]:
            
            # Windows is fucking stupid why would you use backslashes
            paths = {
                "config": environ["APPDATA"] + "\\tadr",
                "data": environ["APPDATA"] + "\\tadr\data"
            } if os == "win" else {
                "config": home + "/.config/tadr",
                "data": home + "/.tadr/data"
            }
                
            #Create any missing paths/directories
            for path in paths:
                if not isdir(paths[path]):
                    Log.new(f"Making path: {paths[path]}")
                    for directory in paths[path].split("/")[1:]:
                       if not isdir(paths[path].split(directory)[0] + directory):
                           Log.new(f"Making directory: {paths[path].split(directory)[0]}{directory}")
                           mkdir(paths[path].split(directory)[0] + directory)
            return paths
        
        # Exit is OS is unsupported
        else:
            Log.new(Log.warning(f"Unsupported operating system: {os}, exiting."))
            exit()
