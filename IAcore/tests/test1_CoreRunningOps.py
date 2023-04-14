""" Test CoreRunningOps class
"""
import unittest
from IAcore.core.core import CoreRunning


class tdd_cases(unittest.TestCase):
    def test_corerunning_lists_operations(self):
        ideal_kwargs = {"mqttclient": "mqttclient",
                        "modbusclient": "modbusclient",
                        "model4horizontalimage": "model4horizontalimage",
                        "model4verticalimage": "model4verticalimage",
                        "model4classification": "model4classification",
                        "sendwaitingstate2plc": "sendwaitingstate2plc",
                        "startiacoreplcconnectionloop": "startiacoreplcconnectionloop",
                        "op_mode": "list_ops"
                       }
        kwargs = CoreRunning.call_operations(op_mode="list_ops")
        self.assertEqual(ideal_kwargs, kwargs)


if __name__ == "__main__":
    unittest.main()








