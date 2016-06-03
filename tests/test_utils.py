from unittest import TestCase

from videodata import utils


class UtilsTestCase(TestCase):
    def test_order_dict(self):
        dictionary = {
            'a': 1,
            'b': 3,
            '0': 2,
            'z': 0,
        }

        sort_using = ('z', 'a', '0', 'b')

        ordered_dict = utils.order_dict(dictionary, sort_using)

        self.assertEqual(sort_using, tuple(ordered_dict.keys()))
