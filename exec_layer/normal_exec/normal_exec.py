# ---------- IMPORTS ----------

import datetime
import pyautogui as pag
import webbrowser
import urllib.parse
from exec_layer.normal_exec.int_check import is_connected
#import operator

import subprocess, os, sys
#import threading
#import requests
import time
import json
import re

# ---------- HASHMAP SETUP ----------

APP_REG_FILE = f"assets/system/app_registry.json"
command_registry = {}
app_registry = {}

def register(name):
    def decorator(func):
        command_registry[name] = func
        return func
    return decorator

with open(APP_REG_FILE, "r") as file:
    app_registry = json.load(file)


# DEVELOPER NOTE #----------------------------------------------------------------------------------
# Most of these functions were created keeping in mind macOS (Apple Sillicon) functionality in mind.
# Windows-Compatible Versions (and maybe even a Linux compatible version) will be coming out soon.
#---------------------------------------------------------------------------------------------------


# ---------- HELPER FUNCTION DEFINITIONS ----------

def get_active_app():
    script = 'tell application "System Events" to get name of first application process whose frontmost is true'
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def find_app(name: str):
    try:
        result = subprocess.run(
            [
                "mdfind",
                f"kMDItemKind == 'Application' && kMDItemDisplayName == '*{name}*'"
            ],
            capture_output=True,
            text=True)
        apps = result.stdout.strip().split("\n")
        if apps and apps[0]:
            return os.path.basename(apps[0]).replace(".app", "")
        return None
    except Exception as e:
        print("Search error:", e)
        return None

def get_app(target: str):
    for app, data in app_registry.items():
        if target.lower() == app or target.lower() in data["aliases"]:
            if data["name"] == "current_app":
                return get_active_app()
            return str(data["name"])
    found = find_app(target)
    if found:
        return found
    return target

# ---------- DEFAULT FUNCTION DEFINITIONS ----------

@register("open_app")
def open_app(target: str) -> bool:
    '''
    Opens applications on the user device.

    Args:
        target (str): Name of app you want to OPEN.

    Returns:
        bool: Success status of opening the app.
    '''
    if not target:
        return False
    try:
        target = get_app(target=target)
        subprocess.run(["open", "-a", target], check=True)
        return True
    except Exception as e:
        print(f"[ERR - open_app]: {e}")
        return False


@register("close_app")
def close_app(target: str) -> bool:
    '''
    Closes applications on the user device.

    Args:
        target (str): Name of app you want to CLOSE.

    Returns:
        bool: Success status of closing the app.
    '''
    if not target:
        return False
    try:
        target = get_app(target=target)
        applescript = f'tell application "{target}" to quit'
        subprocess.run(["osascript", "-e", applescript], check=True)
        #os.system(f"osascript -e '{applescript}'") -> soft depriciated
        return True
    except Exception as e:
        print(f"[ERR - close_app]: {e}")
        return False


@register("get_current_time")
def get_current_time() -> str:
    '''
    Function to get the current time.

    Returns:
        time (str): Current time.
    '''
    time = datetime.datetime.now().strftime("%-I:%M %p")
    return time


@register("get_current_date")
def get_current_date() -> str:
    '''
    Function to get the current date.

    Returns:
        date (str): Today's Date.
    '''
    date = datetime.date.today()
    return date


@register("get_current_day")
def get_current_day() -> str:
    '''
    Function to get today's day. (eg. Sunday, Monday)

    Returns:
        day (str): Today's Day
    '''
    day = datetime.datetime.now().strftime("%A")
    return day


@register("take_screenshot")
def take_screenshot(filename: str) -> bool:
    '''
    Function to take a screenshot.

    Args:
        filename (str): Name of the file (or path) you want to save the screenshot as.

    Returns:
        status (bool): Status of taking a screenshot.
    '''
    filepath = os.path.join("Screenshots", filename)
    try:
        subprocess.run(["screencapture", filepath], check=True) 
        return True
    except:
        return False


@register("get_battery_information")
def get_battery_information() -> dict:
    '''
    Function to get power/battery levels/information of the user device.

    Returns:
        battery_information (dict): Various information regarding the device battery level.
    '''
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True
        )
        match = re.search(r'(\d+)%;\s*(\w+);\s*([\d:]+ remaining|no estimate)', result.stdout)
        if not match:
            return None
        percentage = int(match.group(1))
        charging_status = match.group(2).lower()
        time_remaining = match.group(3)
        return {
            "percentage": percentage,
            "status": charging_status,
            "time_remaining": time_remaining
        }
    except Exception as e:
        print(f"[ERR - battery]: {e}")
        return None


@register("open_link")
def open_link(url: str) -> bool:
    '''
    Function to open a link in the browser or open web apps in the browser.

    Args:
        url (str): link the user wants to search for. (eg. youtube.com)
    
    Returns:
        status (bool): Success status of opening link.
    '''
    if not url:
        return False
    try:
        target = url.strip()
        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        webbrowser.open(target, new=2)
        return True
    except Exception as e:
        print(f"[ERR - open_link]: {e}")
        return False


@register("search_youtube")
def search_youtube(query: str) -> bool:
    '''
    Function to search on YouTube.

    Args:
        query (str): String to search on youtube for.

    Returns:
        status (bool): Success status of searching on YouTube.
    '''
    if not query:
        return False
    try:
        encoded = urllib.parse.quote(query.strip())
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url, new=2)
        return True
    except Exception as e:
        print(f"[ERR - search_yt]: {e}")
        return False


@register("search_web")
def search_web(query: str) -> bool:
    '''
    Function to search for a general query on the browser.

    Args:
        query (str): What the user wants to search for. (eg. How to bake a cake?)

    Returns:
        status (bool): Success status of searching the web.
    '''
    if not query:
        return False
    try:
        encoded = urllib.parse.quote(query.strip())
        url = f"https://duckduckgo.com/?q={encoded}"
        webbrowser.open(url, new=2)
        return True
    except Exception as e:
        print(f"[ERR - search_web]: {e}")
        return False


@register("check_internet")
def check_internet() -> bool:
    """
    Check if the device is connected to the internet.

    Returns:
        status (bool): Status of Internet Connection.
    """
    return is_connected()


@register("open_file")
def open_file(path: str) -> bool:
    """
    Open a file or folder.

    Args:
        path (str): Path to file or folder. (use local path r\"Screenshots/<filename>\" for Screenshots)

    Returns:
        status (bool): Success status of opening the file.
    """
    if not path:
        return False
    try:
        subprocess.run(["open", path], check=True)
        return True
    except Exception as e:
        print(f"[ERR - open_file]: {e}")
        return False


@register("set_volume")
def set_volume(level: int) -> bool:
    """
    Set system volume.

    Args:
        level (int): Volume level (0-100)

    Returns:
        status (bool): Success status of changing the volume.
    """
    try:
        level = int(level)
        level = max(0, min(100, level))
        subprocess.run([
            "osascript",
            "-e",
            f"set volume output volume {level}"
        ], check=True)
        return True
    except Exception as e:
        print(f"[ERR - set_vol]: {e}")
        return False


@register("wait_function")
def wait_function(seconds: int) -> None:
    '''
    Function to wait for the given amount of time in seconds.

    Args:
        seconds (int): The number of seconds you want to wait for.

    Returns:
        None
    '''
    time.sleep(seconds)

@register("shutdown")
def shutdown() -> None:
    '''
    Function to exit the program and shutdown EVA. (IF user says goodbye or asks to exit/shutdown).

    Returns:
        None
    '''
    exit()

# ---------- PLUGIN FUNCTION DEFINITIONS ----------

# >> For USER to Add Custom Functions
# Make sure to provide proper docstrings to each function. --> Helps LLM with tool-calling

# ---------- MAIN EXEC ----------

def request_exec(query):
    try:
        intent = query["intent"]
        kwargs = query["parameters"]
        if intent in command_registry:
            command_registry[intent](**kwargs)
            return True
        else:
            return False
    except:
        return False

#*---------- END OF CODE ----------*