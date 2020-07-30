"""
Copyright 2020 Christopher Andrews

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os.path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

# TODO: Allow users to automatically upload to cloud storage like AWS S3
# TODO: Make a way to gracefully kill chrome process in case of sudden program exit
class Driver:
    def __init__(self, driver_path, output_path, delay, uri_dict):
        # If user provides a path to the webdriver, then use it, otherwise search PATH, else throw an error
        if driver_path != "" and isinstance(driver_path, str):
            self.driver_path = driver_path
        elif driver_path == None:
            self.driver_path = "chromedriver"
        elif driver_path == "chromedriver":
            self.driver_path = "chromedriver"
        else:
            raise TypeError("driver_path must be either None or of type (str) and cannot be empty")

        # Check if output path is a valid directory
        if output_path != "" and output_path != None and isinstance(output_path, str):
            if os.path.exists(output_path):
                self.output_path = output_path
            else:
                raise NotADirectoryError("output_path: %s is not a valid directory" % output_path)
        else:
            raise TypeError("output_path must not be empty and must be of type (str)")

        # Set the delay between page gets in seconds
        if delay != None and isinstance(delay, int):
            if delay < 2:
                self.delay = 2
                print("Warning, delay argument was less than default value, setting to 2 seconds")
            else:
                self.delay = delay
        elif delay == None:
            self.delay = 2
        else:
            raise TypeError("delay must be of either type (int) or type (None)")

        # The dictionary comprised of file_name[uri]
        if uri_dict != None and isinstance(uri_dict, dict):
            self.uri_dict = uri_dict
        else:
            raise TypeError("uri_dict must be of type dict")

        # Get correct path of web driver
        # TODO: Consider only using webdriver found in PATH
        self.DRIVER = self.driver_path

        # Set the default driver instance
        driver_options = Options()
        driver_options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.DRIVER, options=driver_options)
        

    # Gets the page, gets the max scrolling height of the browser window and resizes it
    def _get_uri(self, uri):
        self.driver.get(uri)

    # Gets the max scroll height of the current page
    def _get_height(self):
        return self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")

    # Resets the default window size, this is so that each time we load a page, it uses the corret height of the page, instead of the last highest value
    def _reset_default_window_size(self):
        self.driver.set_window_size(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    # Given a height, resize the current browser window in-place
    def _resize_window(self, height):
        self.driver.set_window_size(DEFAULT_WIDTH, height, windowHandle='current')

    # Gets the current output_filepath based on file_name supplied
    def _build_path(self, file_name):
        return os.path.join(self.output_path, "%s.png" % file_name)

    # Take a screenshot and save as output file
    def _screenshot(self, file_name):
        self.driver.save_screenshot(file_name)

    # Shutdown the chromium instance
    def _shutdown(self):
        print(">>> SHUTTING DOWN BROWSER")
        self.driver.quit()

    # Given a height, url and an article_id, it will open the url at the chosen height and take a screenshot
    def run(self):
        for file_name, uri in self.uri_dict.items():
            print(">>> TAKING SCREENSHOT OF %s" % uri)
            self._get_uri(uri)
            self._reset_default_window_size()
            height = self._get_height()
            self._resize_window(height)
            file_name = self._build_path(file_name)
            self._screenshot(file_name)
            print(">>> SUCCESS")
        self._shutdown()