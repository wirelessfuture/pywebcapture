import pytest

from loader import FileLoader

def file_load():
    fl = FileLoader("example3.csv", True, 3, "web-scraper-order")

def f():
    raise SystemExit(1)

def test_exception():
    with pytest.raises(FileNotFoundError):
        f()