# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.utils.serialize import ScrapyJSONEncoder

from videodata.utils import slugify, order_dict
from videodata.items import VideoItem, CategoryItem


class PyVideoJsonWriterPipeline:
    encoder = ScrapyJSONEncoder(indent=2, ensure_ascii=False, sort_keys=False)

    # since PyVideo cares about the fields order and Scrapy doesn't support that, let's define it here:
    category_fields_order = (
        'title',
        'description',
        'url',
        'start_date',
        'slug',
    )

    video_fields_order = (
        'category',
        'slug',
        'title',
        'summary',
        'description',
        'quality_notes',
        'language',
        'copyright_text',
        'thumbnail_url',
        'duration',
        'videos',
        'source_url',
        'tags',
        'speakers',
        'recorded',
    )

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            event_name = slugify(item['title'])
            event_path = os.path.join(spider.settings['OUTPUT_DIR'], event_name)
            os.makedirs(event_path, exist_ok=True)
            category_json_path = os.path.join(event_path, 'category.json')
            with open(category_json_path, 'w') as fp:
                fp.write(self.encoder.encode(order_dict(item, self.category_fields_order)))

        elif isinstance(item, VideoItem):
            event_name = slugify(item['category'])
            videos_path = os.path.join(spider.settings['OUTPUT_DIR'], event_name, 'videos')
            os.makedirs(videos_path, exist_ok=True)
            video_json_path = os.path.join(videos_path, '{}.json'.format(slugify(item['title'])))
            with open(video_json_path, 'w') as fp:
                fp.write(self.encoder.encode(order_dict(item, self.video_fields_order)))

        return item
