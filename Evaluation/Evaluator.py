from Evaluation.EvaluatorBehaviorInterface import EvaluatorBehaviorInterface

__author__ = 'Malte-Christian'


class Evaluator:
    def __init__(self, log_data_queue):
        self._log_data_queue = log_data_queue
        self._log_data = {}
        self._behaviors = []

    """
    Adds behavior to evaluator (e.g. delay, throughput,...)
    """
    def add_behavior(self, behavior):
        if isinstance(behavior, EvaluatorBehaviorInterface):
            self._behaviors.append(behavior)
        else:
            raise Exception('Wrong Interface.')

    def _refresh_data(self):
        # Get latest log data from queue
        print self._log_data
        while True:
            try:
                data = self._log_data_queue.get(block=False)

                # Initialise node log table if not exist
                try:
                    self._log_data[int(data['node_id'])]
                except KeyError:
                    self._log_data[int(data['node_id'])] = {}

                try:
                    # Merge with existing log data
                    self._log_data[int(data['node_id'])][int(data['log_id'])].update(data['data'])
                except KeyError:
                    # Add new log data
                    self._log_data[int(data['node_id'])][int(data['log_id'])] = data['data']

            except Exception:
                break

    def get_results(self, short=False):
        self._refresh_data()
        result = []
        for behavior in self._behaviors:
            result.append(behavior.analyse(self._log_data, short))

        return result

    def get_short_result(self):
        return self.get_results(True)