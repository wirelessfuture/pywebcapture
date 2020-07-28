"""
Copyright 2020 Christopher Andrews

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import csv
from urllib.parse import urlparse

# CSVLoader takes a valid .csv file and builds a filename/uri map for the driver
class CSVLoader:
    def __init__(self, input_filepath, has_header, uri_column, filename_column):
        # User must pass a valid csv file as the input_filepath argument as type str
        if input_filepath != "" and input_filepath != None and isinstance(input_filepath, str):
            if os.path.isfile(input_filepath):
                self.input_filepath = input_filepath
            else:
                raise FileNotFoundError("input_filepath %s is not a file!" % input_filepath)
        elif input_filepath.lower().endswith(".csv") != True:
            raise Exception("input_filepath must be a valid *.csv file")
        else: 
            raise TypeError("input_filepath must be of type (str) and cannot be empty or None")

        # Check if file has a header or not and represent with bool
        # TODO: Use csv.Sniffer().has_header as a fallback method if chosen
        if has_header is True or has_header is False:
            self.has_header = has_header
        else:
            raise TypeError("has_header must be of type (bool)")

        # Allow users to pass the name of the column or the index of the column that contains the uri list, else raise exception
        # TODO: Add regex for detecting valid URI
        if uri_column != "" and uri_column != None and isinstance(uri_column, str):
            self.uri_column = self._translate_column_to_index(uri_column)
        elif isinstance(uri_column, int):
            self.uri_column = uri_column
        else:
            raise TypeError("uri_column must be either column name of type (str) or index of column of type (int)")

        # Check if filename column is given, if empty or None, then assume that the filename is included in the uri
        if filename_column != "" and filename_column != None and isinstance(filename_column, str):
            self.filename_column = self._translate_column_to_index(filename_column)
        elif isinstance(filename_column, int):
            self.filename_column = filename_column
        else:
            self.filename_column = None

        # Create an empty dict
        self.uri_dict = {}


    # Translate the column name from the csv as an index of type (int), if not found, raise Exception
    def _translate_column_to_index(self, column_name):
        if self.has_header == True:
            with open(self.input_filepath, 'r', encoding='utf-8') as in_file:
                reader = csv.reader(in_file)
                for i, line in enumerate(reader):
                    if i < len(line):
                        if column_name in line[i]:
                            return i
                raise Exception("Could not locate filename column: %s" % column_name)
        else:
            raise Exception("Cannot convert column name string to index, input_file does not have a header!")

    # Private method, loads and sets the internal uri_dict variable
    def _set_uri_dict(self):
        with open(self.input_filepath, 'r', encoding='utf-8') as in_file:
            uri_dict_temp = {}
            reader = csv.reader(in_file)

            # If the filename is not specified, use netloc as filename + index of iteration
            if self.filename_column == None:
                # Exclude header if has_header is True
                if self.has_header == True:
                    next(reader)
                    for i, line in enumerate(reader):
                        parsed_uri = urlparse(line[self.uri_column]).netloc.replace(".", "_").replace(':', "_")
                        uri_dict_temp[parsed_uri + "_%i" %i] = line[self.uri_column]
                else:
                    for i, line in enumerate(reader):
                        parsed_uri = urlparse(line[self.uri_column]).netloc.replace(".", "_").replace(':', "_")
                        uri_dict_temp[parsed_uri + "_%i" %i] = line[self.uri_column]

            # Exclude header if has_header is True
            elif isinstance(self.filename_column, int):
                if self.has_header == True:
                    next(reader)
                    for line in reader:
                        uri_dict_temp[line[self.filename_column]] = line[self.uri_column]
                        print("I HAVE A HEADER")
                else:
                    for line in reader:
                        uri_dict_temp[line[self.filename_column]] = line[self.uri_column]
                        
            # Replace dict with temp dict
            self.uri_dict = uri_dict_temp            

    # Get the uri dict
    def get_uri_dict(self):
        self._set_uri_dict()
        return self.uri_dict