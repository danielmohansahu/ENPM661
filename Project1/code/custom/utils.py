""" Miscellaneous utility function / classes
"""
import time
import csv

class Timer(object):
    def __init__(self, description, debug=False):
        self.description = description
        self.debug = debug
    def __enter__(self):
        if self.debug:
            self.start = time.time()
    def __exit__(self, type, value, traceback):
        if self.debug:
            self.end = time.time()
            print(f"{self.description}: {self.end - self.start}")

def to_file(string, filename):
    """Print given string object to a file.
    """
    with open(filename, "w") as txtfile:
        txtfile.write(string)
