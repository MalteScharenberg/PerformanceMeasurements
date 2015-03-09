import multiprocessing
import time
import json
import sys

from Node.NodeClass import NodeClass
from Evaluation.Evaluator import Evaluator
from Helper.Printer import Printer
from Helper.MatlabExporter import MatlabExporter
from Hardware.HardwareMock import HardwareMock
from Node.Source import Source
from Node.Sink import Sink
from Evaluation.Throughput import Throughput
from Evaluation.Delay import Delay

__author__ = 'Malte-Christian'


if __name__ == '__main__':
    log_data_queue = multiprocessing.Queue()
    evaluator = Evaluator(log_data_queue)

    printer = Printer()
    nodes = []

    # Parse config file
    try:
        config = json.load(open('config.json'))
        matlab_exporter = MatlabExporter(config['matlab_exporter']['file'])
        for behavior in config['evaluator_behaviors']:
                behavior = globals()[behavior['type']](**behavior['arguments'])
                evaluator.add_behavior(behavior)
        for node_config in config['nodes']:
            hardware = globals()[node_config['hardware']['type']](**node_config['hardware']['arguments'])
            node = NodeClass(log_data_queue, hardware)
            for behavior in node_config['behaviors']:
                behavior = globals()[behavior['type']](**behavior['arguments'])
                node.add_behavior(behavior)
            nodes.append(node)
    except KeyError, e:
        print 'Key Error in config file:', e
        sys.exit(1)
    except TypeError, e:
        print 'Type Error in config file:', e
        sys.exit(1)

    # Start node processes
    map(NodeClass.start, nodes)

    # source.join()
    # print('ende')
    try:
        while True:
            results = evaluator.get_short_results()
            printer.print_short_results(results)
            time.sleep(1)
    except KeyboardInterrupt:
        results = evaluator.get_results()
        printer.print_results(results)
        matlab_exporter.export(results)