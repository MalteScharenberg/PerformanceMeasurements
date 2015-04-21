__author__ = 'Malte-Christian Scharenberg'

import math
from Evaluation.IEvaluatorBehavior import IEvaluatorBehavior


class Delay(IEvaluatorBehavior):
    def __init__(self, node_id, block_size, group_by=False):
        self.node_id = int(node_id)
        self.block_size = block_size
        self.group_by = group_by

    def get_name(self):
        return self.__class__.__name__ + ' Node ' + str(self.node_id)

    def analyze(self, data, short):
        try:
            node_data = data[self.node_id]
        except KeyError:
            return

        # Filter input data
        node_data = filter(lambda date: 'received_time' in date
                                        and (not self.group_by or (self.group_by in date)),
                           # if 'group_by' is set, it should be a key in date
                           node_data)

        size = len(node_data)
        end = int(math.ceil(size / self.block_size))
        start = end - 1 if short else 0

        if start < 0:
            return

        delay = []
        for n in range(start, end):
            # Sum up delays
            delay_sum = 0
            received_packets = 0
            group_value = None
            for i in range(n * self.block_size, (n + 1) * self.block_size):
                try:
                    # handle grouping
                    # simple implementation...therefore block size in config should match mutation of group value
                    if self.group_by:
                        if group_value is None:
                            group_value = node_data[i][self.group_by]
                        if node_data[i][self.group_by] != group_value:
                            continue

                    delay_sum += node_data[i]['received_time'] - node_data[i]['send_time']
                    received_packets += 1
                except KeyError, e:
                    print 'Key error: %s' % e.message

            if self.group_by:
                desc = 'mean of {0} packets grouped by \'{1}\' = {2}'.format(received_packets, self.group_by,
                                                                             group_value)
            else:
                desc = 'mean of {0} packets'.format(received_packets)

            delay.append(dict(data=delay_sum / received_packets,
                              desc=desc))

        result = dict(data=delay,
                      dimension='s')

        return result