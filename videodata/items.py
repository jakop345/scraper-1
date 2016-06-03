# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoField(scrapy.item.Field):
    """Video contains the information about the type and location of the video"""

    # video's URL
    url = scrapy.Field()

    # video's length in seconds
    length = scrapy.Field()

    # video's type/source (like: youtube)
    video_type = scrapy.Field()


class VideoItem(scrapy.Item):
    """Video item describes a talk"""

    # category is an event name
    category = scrapy.Field()

    # slugified title
    slug = scrapy.Field()

    # talk name
    title = scrapy.Field()

    # talk summary
    summary = scrapy.Field()

    # talk description
    description = scrapy.Field()

    # denotes issues with the quality (things like "no sound", "picture cuts out 3:15 in", etc...)
    quality_notes = scrapy.Field()

    # full language name, like English
    language = scrapy.Field()

    # license for the talk's video
    copyright_text = scrapy.Field()

    # URL for the thumbnail
    thumbnail_url = scrapy.Field()

    # talk duration in seconds
    duration = scrapy.Field()

    # list of available videos
    videos = VideoField()

    # link to the talk's/event's page
    source_url = scrapy.Field()

    # talks keywords, like 'git', 'lib-name'
    tags = scrapy.Field()

    # list of speakers' names
    speakers = scrapy.Field()

    # string representation of the date of the recording
    recorded = scrapy.Field()


class CategoryItem(scrapy.Item):
    """Category item describes an event"""

    # event's name
    title = scrapy.Field()

    # event's description
    description = scrapy.Field()

    # event's home page URL
    url = scrapy.Field()

    # date of the event (YYYY-MM-DD)
    start_date = scrapy.Field()

    # slugified event's name
    slug = scrapy.Field()
