from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class PageDriver:
    # Initialise the drivers
    def __init__(self, output_path):
        self.DRIVER = 'chromedriver'
        height_driver_options = Options()
        height_driver_options.add_argument("--headless")
        self.height_driver = webdriver.Chrome(self.DRIVER, options=height_driver_options)
        self.screen_driver = None

        if output_path != "" or output_path != None:
            self.output_path = output_path
        else:
            self.output_path = None

    # Given a height, sets a new selenium driver with new options
    def set_screen_driver(self, height):
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
    def screenshot_page(self, height, url, article_id):
        try: 
            print(f">>> TAKING SCREENSHOT OF {url}")
            self.set_screen_driver(height)
            self.screen_driver.get(url)

            if self.output_path != None:
                current_output_path = os.path.join(self.output_path, f'{article_id}.png')
                self.screen_driver.save_screenshot(current_output_path)
            else: 
                self.screen_driver.save_screenshot(f'{article_id}.png')

            print(">>> SUCCESS")
        except Exception:
            print(">>> SOMETHING WENT WRONG, SKIPPING...")
            return