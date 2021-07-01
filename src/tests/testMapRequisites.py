import unittest
import json
import src.utils.MapRequisites as reqMap


class TestMapRequisites(unittest.TestCase):
    def setUp(self):
        with open('../data/courses.json', 'r') as f:
            self.courses = json.dumps(f.read())

    def test_single_course_req(self):
        result = reqMap.mapRequisites(self.courses)
        self.assertEqual(len(result) == )


if __name__ == '__main__':
    unittest.main()
