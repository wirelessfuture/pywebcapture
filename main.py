from driver import PageDriver as pd
from loader import  FileLoader as fl

if __name__ == "__main__":
    fl = FileLoader('example.csv')
    fl.set_articles()
    articles = fl.get_articles()
    pd = PageDriver(output_path='./screenshots')
    for url in articles:
        print(url)
        height = pd.get_page_height(url)
        article_id = url.split("/")[4]
        pd.screenshot_page(height, url, article_id)
        time.sleep(2)
    