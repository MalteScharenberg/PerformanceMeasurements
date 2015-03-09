__author__ = 'Malte-Christian'

import scipy.io as sio

class MatlabExporter:
    def __init__(self, file):
        self.file = file

    def export(self, results):
        sio.savemat(self.file, results)