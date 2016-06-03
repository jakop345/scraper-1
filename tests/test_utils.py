from unittest import TestCase
from collections import OrderedDict

from videodata.spiders import youtube_playlist
from videodata import utils


class TextToolsTestCase(TestCase):
    def test_extract_speakers_empty(self):
        text = '''Intro'''

        speakers = youtube_playlist.extract_speakers(text)

        self.assertEqual([], speakers)

    def test_extract_speakers_single(self):
        text = '''
        Intro
        Speaker: First Speaker
        Outro
        '''

        speakers = youtube_playlist.extract_speakers(text)

        self.assertEqual(['First Speaker'], speakers)

    def test_extract_speakers_multiple(self):
        text = '''
        Intro
        Speakers: First Speaker, 高 國棟, Łąki Łan
        Outro
        '''

        speakers = youtube_playlist.extract_speakers(text)

        self.assertIn('First Speaker', speakers)
        self.assertIn('高 國棟', speakers)
        self.assertIn('Łąki Łan', speakers)

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
