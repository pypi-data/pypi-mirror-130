"""
test_requests.py
====================================
Unit testing for requests module
"""

import unittest
from imath_requests.requests import PartData


class TestRequests(unittest.TestCase):
    """
    Unit testing for requests module.

    """

    def test_part_data_json(self):
        """
        Tests part data json generation.

        """
        # TODO add test for part data json
        # test_part_data_json = {
        #     "timestamp": "1516193959559",
        #     "part_id": "Part1234",
        #     "source": "I3DR_DESKTOP_ABC123",
        #     "part_data": [
        #         {
        #             "key": "steel_grade",
        #             "value": "Grade01"
        #         },
        #         {
        #             "key": "analysis",
        #             "value": [
        #                 {
        #                     "key": "C",
        #                     "value": "0.2"
        #                 },
        #                 {
        #                     "key": "Mn",
        #                     "value": "0.02"
        #                 }
        #             ]
        #         }]
        # }

        # part_data_keys = [
        #     {
        #         "key": "steel_grade",
        #         "value": "Grade01"
        #     },
        #     {
        #         "key": "analysis",
        #         "value": [
        #             {
        #                 "key": "C",
        #                 "value": "0.2"
        #             },
        #             {
        #                 "key": "Mn",
        #                 "value": "0.02"
        #             }
        #         ]
        #     }
        # ]
        # part_data = PartData(
        #     "1516193959559", "Part1234", "I3DR_DESKTOP_ABC123", part_data_keys)
        # self.assertEqual(part_data, test_part_data_json)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
