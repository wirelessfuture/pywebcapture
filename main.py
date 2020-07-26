from driver import PageDriver as pd
from loader import  FileLoader

from itertools import islice

if __name__ == "__main__":
    fl = FileLoader("example.csv", True, 3, "web-scraper-order")
    uri_dict = fl.get_uri_dict()
    print(list(islice(uri_dict.items(), 10)))

    # articles = fl.get_articles()
    # pd = pd(output_path='/screenshots')
    # for url in articles:
    #     print(url)
    #     height = pd.get_page_height(url)
    #     article_id = url.split("/")[4]
    #     pd.screenshot_page(height, url, article_id)
    #     time.sleep(2)
    