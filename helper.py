import os

def return_driver_path():
    if os.name == "nt":
        return ".\chromedriver"
    if os.name == "posix":
        return "./chromedriver"