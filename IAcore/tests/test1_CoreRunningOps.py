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
                        "init":"init"
                       }
        kwargs = CoreRunning.call_operations(init = "init")
        self.assertEqual(ideal_kwargs, kwargs)


if __name__ == "__main__":
    unittest.main()








