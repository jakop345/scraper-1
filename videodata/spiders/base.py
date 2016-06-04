import re

import scrapy


class BaseSpider(scrapy.Spider):
    def parse(self, response):
        raise NotImplementedError

    def __init__(self, *args, speakers_hint=None, **kwargs):
        """
        :param speakers_hint : a value in "<attr>:<sep>:<regex>" format, where:
            - attr : is an attribute name where to look for the speakers list
            - sep : a string used as a separator between speakers
            - regex : a regular expression extracting the speakers

            Example:
                -a 'speakers_hint=item:&:title:&:\((.*)\)$'

                will extract speakers (separated by &) from the end of the title like "Some Title (speaker1 & speaker2)"
        """
        super().__init__(*args, **kwargs)
        self._speakers_hint = speakers_hint

    def extract_speakers(self, item):
        if not self._speakers_hint:
            return []

        attr, sep, regex = self._speakers_hint.split(':', maxsplit=2)

        speakers = []
        for match in re.findall(regex, item[attr], re.IGNORECASE):
            speakers += match.split(sep)

        return [val.strip() for val in speakers]
