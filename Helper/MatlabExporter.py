__author__ = 'Malte-Christian Scharenberg'

import scipy.io as sio


class MatlabExporter:
    def __init__(self, export_file):
        self.file = export_file

    def export(self, results):
        results = map(lambda date: date['data'], results['Delay Node 1']['data'])
        sio.savemat(self.file, dict(
            results=results))