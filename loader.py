import os.path
import csv

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