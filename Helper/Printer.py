__author__ = 'Malte-Christian'

import sys

class Printer():

    def __init__(self):
       pass

    def printl(self, output):
        print output

    """
    Print things to stdout on one line dynamically
    """
    def print_results(self, results):
        sys.stdout.write("\r\x1b[K\r\x1b[K" + str(results))
        sys.stdout.flush()
