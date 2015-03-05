from performanceMeasurement.Evaluation import EvaluatorBehaviorInterface

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
            self.behaviors.append(behavior)
        else:
            raise Exception('Wrong Interface.')

    def _refresh_data(self):
        # Get latest log data from queue
        while True:
            try:
                data = self._log_data_queue.get(block=False)

                try:
                    self._log_data[data['log_id']].update(data['data'])  # Merge with existing log data
                except KeyError:
                    self._log_data[data['log_id']] = data['data']  # Add new log data

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