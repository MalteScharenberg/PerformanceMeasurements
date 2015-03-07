import multiprocessing
import time
import json
import sys

from Node.NodeClass import NodeClass
from Evaluation.Evaluator import Evaluator
from Helper.Printer import Printer


__author__ = 'Malte-Christian'


if __name__ == '__main__':
    log_data_queue = multiprocessing.Queue()
    evaluator = Evaluator(log_data_queue)
    printer = Printer()
    nodes = []

    # Parse config file
    try:
        config = json.load(open('config.json'))
        for node_config in config['nodes']:
            hardware = globals()[node_config['hardware']['type']](**node_config['hardware']['arguments'])
            node = NodeClass(log_data_queue, hardware)
            for behavior in node_config['behaviors']:
                behavior = globals()[behavior['type']](**behavior['arguments'])
                node.add_behavior(behavior)
            nodes.append(node)
    except KeyError, e:
        print 'Error in config file:', e
        sys.exit(1)
    except TypeError, e:
        print 'Error in config file:', e
        sys.exit(1)

    # Start node processes
    map(NodeClass.start, nodes)

    # source.join()
    # print('ende')
    while True:
        results = evaluator.get_results()
        printer.print_results(results)
        time.sleep(1)
