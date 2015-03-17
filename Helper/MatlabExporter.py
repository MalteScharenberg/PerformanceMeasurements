__author__ = 'Malte-Christian Scharenberg'

import scipy.io as sio


class MatlabExporter:
    def __init__(self, export_file):
        self.file = export_file

    def export(self, results):
        sio.savemat(self.file, {'results': results['Delay Node 1']['data']})