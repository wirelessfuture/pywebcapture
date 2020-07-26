import pytest

from loader import FileLoader

class TestLoaderCorrectExceptionRaised:
    def load_file(self, input_filepath, has_header, uri_column, filename_column):
        try:
            fl = FileLoader(input_filepath, has_header, uri_column, filename_column)
        except TypeError:
            raise TypeError
        except FileNotFoundError:
            raise FileNotFoundError

    def test_file_name_not_string(self):
        with pytest.raises(TypeError):
            assert self.load_file(34, True, 3, None)
            assert self.load_file(True, True, 3, None)

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            assert self.load_file("example", True, 3, None)
            assert self.load_file("examplecsv", True, 3, None)

    def test_has_header_is_not_bool(self):
        with pytest.raises(TypeError):
            assert self.load_file("example.csv", "string", 3, None)
            assert self.load_file("example.csv", 42, 3, None)

    def test_uri_column_is_not_string_or_int(self):
        with pytest.raises(TypeError):
            assert self.load_file("example.csv", True, 34.00, None)
            assert self.load_file("example.csv", True, True, None)
            assert self.load_file("example.csv", True, classmethod(), None)