import time
import os.path
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Empty file loader class for reading in urls
class FileLoader:
    def __init__(self, input_file):
        self.input_file = input_file
        self.articles = []

    def set_articles(self):
        with open(self.input_file, 'r', encoding='utf-8') as in_file:
            reader = csv.reader(in_file)
            article_links = []
            for line in reader:
                article_links.append(line[3])
        self.articles = article_links

    def get_articles(self):
        self.articles.pop(0)
        return self.articles


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


if __name__ == "__main__":
    fl = FileLoader('amazon_tv.csv')
    fl.set_articles()
    articles = fl.get_articles()
    pd = PageDriver(output_path='/home/wirel/Development/python_projects/screen_grab_selenium/screenshots')
    for url in articles:
        print(url)
        height = pd.get_page_height(url)
        article_id = url.split("/")[4]
        pd.screenshot_page(height, url, article_id)
        time.sleep(2)
    