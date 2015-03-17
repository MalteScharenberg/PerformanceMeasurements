__author__ = 'Malte-Christian Scharenberg'

from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class Evaluator:
    def __init__(self, log_data_queue):
        self._log_data_queue = log_data_queue
        self._log_data = {}
        self._behaviors = []

    """
    Adds behavior to evaluator (e.g. delay, throughput,...)
    """

    def add_behavior(self, behavior):
        if isinstance(behavior, IEvaluatorBehavior):
            self._behaviors.append(behavior)
        else:
            raise Exception('Wrong Interface.')

    def _refresh_data(self):
        # Get latest log data from queue
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

    def get_raw_data(self):
        self._refresh_data()
        result = {}

        # Sort log data and transform into list
        for node_data in self._log_data.items():
            result[node_data[0]] = []
            log_ids = node_data[1].keys()
            log_ids.sort()
            for log_id in log_ids:
                result[node_data[0]].append(node_data[1][log_id])

        return result

    def get_results(self, short=False):
        raw_data = self.get_raw_data()
        result = {}
        for behavior in self._behaviors:
            behavior_result = behavior.analyse(raw_data, short)
            if behavior_result:
                result[behavior.get_name()] = behavior_result
        return result

    def get_short_results(self):
        return self.get_results(True)