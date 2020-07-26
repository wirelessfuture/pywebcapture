import os.path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from helper import return_driver_path

# Description goes here
# TODO: Allow users to automatically upload to cloud storage like AWS S3
# TODO: Add filetype checking with mimetypes
class PageDriver:
    # Initialise the drivers
    def __init__(self, output_path):
        self.DRIVER = return_driver_path()
        height_driver_options = Options()
        height_driver_options.add_argument("--headless")
        self.height_driver = webdriver.Chrome(self.DRIVER, options=height_driver_options)
        self.screen_driver = None

        # Check if output path is a valid directory, if not then use default screenshots folder
        if output_path != "" and output_path != None and isinstance(output_path, str):
            if os.path.exists(output_path):
                self.output_path = output_path
            else:
                raise NotADirectoryError("output_path: %s is not a valid directory" % output_path)
        else:
            self.output_path = "./screenshots"

    # Given a height, shutsdown the current driver if it exists and sets a new selenium driver with new options
    # It was noted that shutting down the old driver instance would save memory
    # TODO: Kill all chrome webdriver proccesses gracefully on shutdown
    def set_screen_driver(self, height):
        if self.screen_driver != None:
            self.screen_driver.quit()
            self.screen_driver = None
        screen_driver_options = Options()
        screen_driver_options.add_argument("--headless")
        screen_driver_options.add_argument(f"--window-size=1920,{height}")
        screen_driver_options.add_argument("--hide-scrollbars")
        self.screen_driver = webdriver.Chrome(self.DRIVER, options=screen_driver_options)

    # Opens the page in headless mode and attempts to get the scroll height of the page
    def get_page_height(self, url):
        self.height_driver.get(url)
        self.height_driver.maximize_window()
        height = self.height_driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        return height

    # Given a height, url and an article_id, it will open the url at the chosen height and take a screenshot
    def screenshot_page(self, height, uri, file_name):
        try: 
            print(">>> TAKING SCREENSHOT OF %s" % uri)
            self.set_screen_driver(height)
            self.screen_driver.get(uri)

            current_output_path = os.path.join(self.output_path, "%s.png" % file_name)
            self.screen_driver.save_screenshot(current_output_path)

            print(">>> SUCCESS")
        except Exception as err:
            print(">>> SOMETHING WENT WRONG, SKIPPING...")
            print(err)
            return (file_name, uri, height)