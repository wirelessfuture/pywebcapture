import os.path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helper import return_driver_path

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

# Description goes here
# TODO: Allow users to automatically upload to cloud storage like AWS S3
# TODO: Add filetype checking with mimetypes
# TODO: Make a way to gracefully kill chrome process in case of sudden program exit
class PageDriver:
    # Initialise the drivers
    def __init__(self, output_path):
        self.DRIVER = return_driver_path()

        driver_options = Options()
        driver_options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.DRIVER, options=driver_options)

        # Check if output path is a valid directory, if not then use default screenshots folder
        if output_path != "" and output_path != None and isinstance(output_path, str):
            if os.path.exists(output_path):
                self.output_path = output_path
            else:
                raise NotADirectoryError("output_path: %s is not a valid directory" % output_path)
        else:
            self.output_path = "./screenshots"

    # Gets the page, gets the max scrolling height of the browser window and resizes it
    def get_uri(self, uri):
        self.driver.get(uri)

    # Gets the max scroll height of the current page
    def get_height(self):
        return self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")

    # Resets the default window size, this is so that each time we load a page, it uses the corret height of the page, instead of the last highest value
    def reset_default_window_size(self):
        self.driver.set_window_size(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    # Given a height, resize the current browser window in-place
    def resize_window(self, height):
        self.driver.set_window_size(DEFAULT_WIDTH, height, windowHandle='current')

    # Gets the current output_filepath based on file_name supplied
    def build_path(self, file_name):
        return os.path.join(self.output_path, "%s.png" % file_name)

    # Take a screenshot and save as output file
    def screenshot(self, file_name):
        self.driver.save_screenshot(file_name)

    # Shutdown the chromium instance
    def shutdown(self):
        print(">>> SHUTTING DOWN BROWSER")
        self.driver.quit()

    # Given a height, url and an article_id, it will open the url at the chosen height and take a screenshot
    def run(self, uri, file_name):
        print(">>> TAKING SCREENSHOT OF %s" % uri)
        self.get_uri(uri)
        self.reset_default_window_size()
        height = self.get_height()
        self.resize_window(height)
        file_name = self.build_path(file_name)
        self.screenshot(file_name)
        print(">>> SUCCESS")