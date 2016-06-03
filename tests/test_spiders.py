import unittest

from videodata.spiders import base


class BaseSpiderTestCase(unittest.TestCase):
    def test_extract_speakers_empty(self):
        item = {
            'text': 'Intro'
        }

        spider = base.BaseSpider(name='test', speakers_hint='text:,:speaker[s]?: (.+)')
        speakers = spider.extract_speakers(item)

        self.assertEqual([], speakers)

    def test_extract_speakers_single(self):
        item = {
            'text': '''
            Intro
            Speaker: First Speaker
            Outro
            '''
        }

        spider = base.BaseSpider(name='test', speakers_hint='text:.:speaker[s]?: (.+)')

        speakers = spider.extract_speakers(item)

        self.assertEqual(['First Speaker'], speakers)

    def test_extract_speakers_multiple(self):
        item = {
            'text': '''
            Intro
            Speakers: First Speaker, 高 國棟, Łąki Łan
            Outro
            '''
        }

        spider = base.BaseSpider(name='test', speakers_hint='text:,:speaker[s]?: (.+)')

        speakers = spider.extract_speakers(item)

        self.assertIn('First Speaker', speakers)
        self.assertIn('高 國棟', speakers)
        self.assertIn('Łąki Łan', speakers)
