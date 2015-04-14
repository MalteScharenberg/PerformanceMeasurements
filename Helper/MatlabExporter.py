__author__ = 'Malte-Christian Scharenberg'

import scipy.io as sio
import numpy


class MatlabExporter:
    def __init__(self, export_file):
        self.file = export_file

    def export(self, results):
        mean = []

        for key, value in results.iteritems():
            if 'Throughput' in key:
                mean.append(numpy.mean(value['data']))

        sio.savemat(self.file, dict(
            results=numpy.mean(mean)))
        # results = map(lambda date: date['data'], results['Delay Node 1']['data'])
        # sio.savemat(self.file, dict(
        # results=results))