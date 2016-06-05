import datetime
import json
import re
from urllib.parse import urljoin

from pycountry import languages
import scrapy

from videodata import items, utils


class VimeoAPIScraper:
    '''This class is meant to be used as a mixin to an actual scraper.

    It has the basic flow of getting video data from vimeo setup, but leaves
    the text processing to lower level classes. Methods that need implemetation
    are listed first. This class itself it specifically not a `scrapy.Scraper`
    because then it would be available as a crawler from the command line
    '''

    VIMEO_API = 'https://api.vimeo.com'

    @classmethod
    def extract_title(cls, video):
        raise NotImplementedError()

    @classmethod
    def extract_speakers(cls, video):
        raise NotImplementedError()

    @classmethod
    def get_event_category(cls):
        '''Return a Category Item'''

        raise NotImplementedError()

    def get_event_url(self, video):
        '''Return the event url associated with this talk'''

        raise NotImplementedError()

    def get_source_url(self, video):
        '''Get the talk / event page associated with this video'''

        raise NotImplementedError()

    def extract_video(self, video):
        language = video['language']
        if language in (None, 'none'):
            language = 'en'

        return items.VideoItem(
            title=self.extract_title(video),
            summary='',
            description=video['description'],
            category=self.get_event_url(video),
            quality_notes='',
            language=languages.get(iso639_1_code=language).name,
            copyright_text=self.LICENSE_TYPES.get(video['license'], video['license']),
            speakers=self.extract_speakers(video),
            thumbnail_url=video['pictures']['sizes'][-1]['link'],
            duration=video['duration'] * 60,  # API gives duration in minutes
            source_url=self.get_source_url(video),
            recorded=video['created_time'][0:10],
            slug=utils.slugify(video['name']),
            tags=video['tags'],
            videos=[items.VideoField(
                length=video['duration'] * 60,  # API gives duration in minutes
                url=video['link'],
                type='vimeo')]
        )

    def parse(self, response):
        '''Parse the API response for a channel'''
        response = response.replace(cls=scrapy.http.TextResponse)
        data = json.loads(response.body_as_unicode())
        if 'paging' in data:
            if data['paging']['previous'] is None:  # Only yield ONE category item
                yield self.get_event_category()
            if data['paging']['next'] is not None:
                yield scrapy.Request(urljoin(self.VIMEO_API, data['paging']['next']),
                    callback=self.parse,
                    headers={'Authorization': 'Bearer {}'.format(self.settings.attributes['VIMEO_API_KEY'].value)})
        else:
            raise ValueError('The API did not contain pagination data?')
        for video in data['data']:
            yield self.extract_video(video)

    def start_requests(self):
        if not hasattr(self, 'CHANNELS'):
            raise AttributeError('Must define the CHANNEL ids to scrape')
        for chan_id in self.CHANNELS:
            yield scrapy.Request('https://api.vimeo.com/channels/{chan_id}/videos?per_page=50'.format(chan_id=chan_id),
                callback=self.parse,
                headers={'Authorization': 'Bearer {}'.format(self.settings.attributes['VIMEO_API_KEY'].value)})


class DjangoCon2015(VimeoAPIScraper, scrapy.Spider):
    """YouTube Playlist Event scraper for PyVideo/PyTube"""

    LICENSE_TYPES = {
        'youtube': 'Standard YouTube Licence',
        'creativeCommon': 'CC-BY',
    }
    CHANNELS = (952478,)

    name = 'djangocon-eu-2015'
    event_name = 'DjangoCon Europe 2015'
    event_description = 'six days of talks, tutorials & code / Cardiff, Wales / 31st May-5th June'
    event_url = 'http://2015.djangocon.eu/'
    event_startdate = datetime.date(2015, 5, 31)
    PARSER_RE = re.compile(r'(?P<speaker>.*)( - |, )(?P<title>.*), at DjangoCon Europe 2015, Cardiff')

    @classmethod
    def extract_title(cls, video):
        groups = cls.PARSER_RE.match(video['name'])
        if groups is None:
            raise ValueError('Error parsing title')
        groups = groups.groupdict()
        return groups['title']

    @classmethod
    def extract_speakers(cls, video):
        groups = cls.PARSER_RE.match(video['name'])
        if groups is None:
            raise ValueError('Error parsing speaker')
        groups = groups.groupdict()
        speakers = groups['speaker'].strip()
        return speakers.split('&')

    @classmethod
    def get_event_category(cls):
        return items.CategoryItem(
            title=cls.event_name,
            description=cls.event_description,
            url=cls.event_url,
            start_date=cls.event_startdate,
            slug=utils.slugify(cls.event_name),
        )

    def get_event_url(self, video):
        return 'DjangoCon Europe 2015'

    def get_source_url(self, video):
        return 'http://2015.djangocon.eu/talks/'
