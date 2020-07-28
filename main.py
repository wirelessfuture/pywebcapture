import time

from driver import Driver as d
from loader import CSVLoader


if __name__ == "__main__":
    csv_file = CSVLoader("example.csv", True, 3, None)
    uri_dict = csv_file.get_uri_dict()
    d = d(None, 3, uri_dict)
    d.run()
    