# Pyscreen
Allows you to loop through a list of uri's and grab a screenshot that can be saved to disk.

## Installation
How to install it here

## Basic Usage

**Import the modules:**

```python
from driver import Driver as d
from loader import CSVLoader
```

**Use the CSVLoader to load your csv file containing the urls and optional file names:**

Options:
* input_filepath - The absolute path to your csv file (str)
* has_header - Whether your csv has a header row or now (bool)
* uri_column - The column that contains the uri's, can use either column name (str) or the index position (int)
* filename_column - The column that contains the desired file names (str), can be set to None, where the driver will use the uri netloc as the filename

```python
csv_file = CSVLoader("example.csv", True, 3, None)
```

**Call the get_uri_dict() method from the CSVLoader instance, this parses the CSV into a Python dictionary:**

```python
uri_dict = csv_file.get_uri_dict()
```

**Create instance of the web driver:**

Options:
* output_path - This is the output path that you want to save screen shots at (str), setting to None will output all files to ./screenshots
* delay - This is the delay in seconds between each page request, minimum is 2 seconds, please crawl pages respectfully :)
* uri_dict - The Python dictionary containing your file names and uri's

```python
d = d(None, 3, uri_dict)
```

**Run the driver, this will loop through all uri's, get the maximum scrollheight and then take a screenshot**

```python
d.run()
```
