__author__ = 'Malte-Christian Scharenberg'

import scipy.io as sio
import numpy


class MatlabExporter:
    def __init__(self, export_file):
        self.file = export_file

    def export(self, results):
        export = {}

        for key, value in results.iteritems():
            if 'ThroughputTime' in key:
                for date in value['data']:
                    if str(date['desc']) not in export:
                        export[str(date['desc'])] = []
                    export[str(date['desc'])].append(date['data'])

        sio.savemat(self.file, export)

        # results = map(lambda date: date['data'], results['Delay Node 1']['data'])
        # sio.savemat(self.file, dict(
        # results=results))