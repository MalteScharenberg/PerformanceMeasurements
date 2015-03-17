__author__ = 'Malte-Christian Scharenberg'

import scipy.io as sio


class MatlabExporter:
    def __init__(self, export_file):
        self.file = export_file

    def export(self, results):
        sio.savemat(self.file, dict(
            results=results['Delay Node 1']['data']['data'] if type(results['Delay Node 1']['data']) is dict else
            results['Delay Node 1']['data']))