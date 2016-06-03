import json
import re
from urllib.parse import urlencode

import scrapy

from videodata import items, utils

from pycountry import languages


EXTRACT_SPEAKERS_RE = re.compile('speaker[s]?: (.+)', re.IGNORECASE)


def extract_speakers(text):
    match = EXTRACT_SPEAKERS_RE.findall(text)

    result = []
    for line in match:
        result += [speaker.strip() for speaker in line.split(',')]

    return result


class YouTubePlaylistEventSpider(scrapy.Spider):
    """YouTube Playlist Event scraper for PyVideo/PyTube"""

    API_BASE_URL = 'https://www.googleapis.com/youtube/v3/'
    API_MAX_RESULTS = 50

    WEB_VIDEO_URL = 'https://www.youtube.com/watch?v={video_id}'
    WEB_PLAYLIST_URL = 'https://www.youtube.com/playlist?list={playlist_id}'

    LICENSE_TYPES = {
        'youtube': 'Standard YouTube Licence',
        'creativeCommon': 'CC-BY',
    }

    name = 'youtube_playlist'

    def __init__(self, playlist_id, api_key=None, *args, **kwargs):
        """To run the spider, it's necessary to pass playlist_id and (optionally) an api_key.

        For example:
        $ scrapy runspider videodata/videodata/spiders/youtube_playlist.py \
            -a playlist_id=<PlaylistID> \
            -a api_key=<GoogleAPIKey>
        """
        super().__init__(*args, **kwargs)

        self.playlist_id = playlist_id

        self.base_url_parameters = {
            'part': 'snippet',
            'maxResults': self.API_MAX_RESULTS,
        }

        if api_key:
            self.base_url_parameters['key'] = api_key

        playlists_url_parameters = self.base_url_parameters.copy()
        playlists_url_parameters['id'] = self.playlist_id

        self.start_urls = [
            self.API_BASE_URL + 'playlists?' + urlencode(playlists_url_parameters),
        ]

    def event_item_builder(self, data):
        """Build Event item"""
        return items.CategoryItem(
            title=data['title'],
            description=data['description'],
            url=self.WEB_PLAYLIST_URL.format(playlist_id=self.playlist_id),
            start_date=data['publishedAt'][0:10],
            slug=utils.slugify(data['title']),
        )

    def parse_video(self, response):
        """Parse Video and build a VideoItem"""
        payload = json.loads(response.body.decode())

        data = payload['items'][0]

        snippet = data['snippet']
        thumbnail = snippet['thumbnails'].get('standard', snippet['thumbnails']['maxres'])

        url = self.WEB_VIDEO_URL.format(video_id=data['id'])
        duration = utils.duration_as_seconds(data['contentDetails']['duration'])

        yield items.VideoItem(
            title=snippet['title'],
            summary='',
            description=snippet['description'],
            category=response.meta['event']['title'],
            quality_notes='',
            language=languages.get(iso639_1_code=snippet.get('defaultAudioLanguage', 'en')).name,
            copyright_text=self.LICENSE_TYPES.get(data['status']['license'], data['status']['license']),
            thumbnail_url=thumbnail['url'],
            duration=duration,
            source_url=url,
            recorded=snippet['publishedAt'][0:10],
            slug=utils.slugify(snippet['title']),
            tags=[],
            speakers=extract_speakers(snippet['description']),
            videos=[{
                'length': duration,
                'url': url,
                'type': 'youtube',
            }]
        )

    def generate_talks_url(self, page_token=None):
        """Generate talks API URL"""
        url_parameters = self.base_url_parameters.copy()
        url_parameters.update({
            'playlistId': self.playlist_id,
        })

        if page_token:
            url_parameters['pageToken'] = page_token

        return self.API_BASE_URL + 'playlistItems?' + urlencode(url_parameters)

    def generate_video_url(self, video_id):
        """Generate Video API URL"""
        url_parameters = self.base_url_parameters.copy()
        url_parameters.update({
            'id': video_id,
            'part': 'snippet,contentDetails,status'
        })

        return self.API_BASE_URL + 'videos?' + urlencode(url_parameters)

    def parse_talks(self, response):
        """Parse talks from the response and handle pagination of the Google API results"""
        data = json.loads(response.body.decode())

        items = data.get('items', [])
        for item in items:
            yield scrapy.Request(self.generate_video_url(item['snippet']['resourceId']['videoId']),
                                 callback=self.parse_video,
                                 meta=response.meta)

        if 'nextPageToken' in data:
            yield scrapy.Request(self.generate_talks_url(page_token=data['nextPageToken']),
                                 callback=self.parse_talks)

    def parse(self, response):
        """Default parser to get the general Event metadata and start the talks scraping"""
        data = json.loads(response.body.decode())

        items = data.get('items', [])

        if len(items) != 1:
            raise ValueError('Playlist `{}` not found!'.format(self.playlist_id))

        event_data = items[0]['snippet']
        yield self.event_item_builder(event_data)

        yield scrapy.Request(self.generate_talks_url(), callback=self.parse_talks, meta={'event': event_data})
