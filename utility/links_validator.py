"""
Check the status of each URL in a CSV file.
"""
import csv
import json
import os
import requests
from datetime import datetime


JSON_FOLDER = "../../pyvideo-data/data"
VIDEOS_FOLDER = "videos"
VIDEOS_JSON_ID = "videos"
VIDEO_JSON_URL = "url"


def check_links(videos):
    status_codes = []
    # Check each url's validity
    for video_id, urls in videos:
        for url in urls:
            try:
                print(url)
                req = requests.head(url)
                status_codes.append((video_id, url, req.status_code))
            except requests.HTTPError as e:
                status_codes.append((video_id, url, e.status_code))
            except requests.ConnectionError as e:
                status_codes.append((video_id, url, "ConnectionError"))
    return status_codes


def get_urls():
    urls = {}
    for folder, dirs, files in os.walk(JSON_FOLDER):
        if os.path.basename(folder) == VIDEOS_FOLDER:
            for jf in files:
                if jf[-5:] == ".json":
                    jsonfile = os.path.join(folder, jf)
                    with open(jsonfile, 'r') as f:
                        vid = json.load(f)
                        identifier = vid['category'] + " - " + vid['title']
                        urls[identifier] = [v[VIDEO_JSON_URL] for v in
                                            vid[VIDEOS_JSON_ID]]
    return urls


def generate_report(data):
    now = datetime.today().strftime("%m_%d_%y_%s")
    with open("report-{0}.csv".format(now), "w") as f:
        writer = csv.writer(f)
        columns = ["title", "url", "status code"]
        writer.writerow(columns)
        writer.writerows(data)


if __name__ == "__main__":
    urls = get_urls().items()
    status_codes = check_links(urls)
    generate_report(status_codes)
