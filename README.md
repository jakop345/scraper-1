PyVideo Scrapers
================

Scrapy to generate the JSON files similar to the original pyvideo-data repo.

Python Version
==============
Python 3.4+

Usage
=====

Scraping YouTube playlist
-------------------------

After activating the virtual environment, simply call:

    scrapy runspider videodata/spiders/youtube_playlist.py \
        -a playlist_id=<playlist_id> \
        [-a api_key=<google_api_key>] \
        [-s OUTPUT_DIR=<output_root_directory>]

where:

* `playlist_id` is a `list` query parameter from the YouTube playlist URL (example: https://www.youtube.com/playlist?list=PLqtzN042QpfcOm_sOXxAixvNs9QWhhX5w)
* `google_api_key` is a secret key for Google APIs (required only if public API usage quota is exhausted) - for more info how to obtain the API key, visit: https://support.google.com/cloud/answer/6158862
* `output_root_directory` a root directory where the scraping results will be stored (default: `<current-working-directory>/scraped_data`)
