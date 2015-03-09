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
    def print_short_results(self, results):
        output = ''
        for result_key in results.iterkeys():
            # Format data string
            dimension = results[result_key]['dimension']
            data = "{0} {1}".format(results[result_key]['data'], dimension)

            output += '{0}: {1} '.format(result_key, data)
        sys.stdout.write("\r\x1b[K\r\x1b[K" + str(output))
        sys.stdout.flush()
