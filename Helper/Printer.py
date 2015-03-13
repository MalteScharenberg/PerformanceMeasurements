__author__ = 'Malte-Christian Scharenberg'

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
        self.print_results(results, True)

    def print_results(self, results, short=False):
        output = ''
        for result_key in results.iterkeys():
            # Format data string
            dimension = results[result_key]['dimension']
            output_data = ''
            for data in results[result_key]['data']:
                output_data += '{0} {1}'.format(data, dimension)
                output_data = output_data if short else output_data + '\n'

            output += (('' if short else '\n') + '{0}:' + ('' if short else '\n') + ' {1} ').format(result_key,
                                                                                                    output_data)
        if not short:
            print output
        else:
            sys.stdout.write("\r\x1b[K\r\x1b[K" + output)
            sys.stdout.flush()