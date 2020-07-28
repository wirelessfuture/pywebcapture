from itertools import islice
import time

from driver import PageDriver as pd
from loader import CSVLoader


if __name__ == "__main__":
    fl = CSVLoader("example.csv", True, 3, None)
    uri_dict = fl.get_uri_dict()
    pd = pd(None)
    for file_name, uri in uri_dict.items():
        pd.run(uri, file_name)
        time.sleep(2)
    pd.shutdown()
    