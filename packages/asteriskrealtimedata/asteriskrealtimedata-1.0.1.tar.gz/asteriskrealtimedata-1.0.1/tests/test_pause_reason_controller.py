import unittest
from AsteriskRealtimeData.infrastructure.api.pause_reason_controller import (
    PauseReasonController,
)


class TestPauseReasonController(unittest.TestCase):
    def test_create_pause_reason_from_controller(self):

        pause_reason_controller = PauseReasonController().create_pause_reason(
            {
                "pause_code": "100001",
                "description": "testing",
                "other_parameter": "another value",
            }
        )
        print(pause_reason_controller)

        # pause_reason = PauseReason("100000", "testing")
        # self.assertEqual(pause_reason.get_pause_code(), "100000")
