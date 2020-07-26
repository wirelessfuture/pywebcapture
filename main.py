from itertools import islice
import time

from driver import PageDriver as pd
from loader import  FileLoader


if __name__ == "__main__":
    fl = FileLoader("example.csv", True, 3, "web-scraper-order")
    uri_dict = fl.get_uri_dict()
    pd = pd(None)
    failed_screenshots = []
    for file_name, uri in uri_dict.items():
        height = pd.get_page_height(uri)
        failed = pd.screenshot_page(height, uri, file_name)
        if failed == None:
            pass
        else:
            failed_screenshots.append(failed)
        time.sleep(2)
    print(failed_screenshots)
    