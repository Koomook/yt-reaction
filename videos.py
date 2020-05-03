import json
import time
from typing import List

import requests
from ycd.downloader import ajax_request, find_value, search_dict, USER_AGENT

YOUTUBE_VIDEOS_AJAX_URL = "https://www.youtube.com/browse_ajax"


def channel_video_url(channel_id: str) -> str:
    return f"https://www.youtube.com/channel/{channel_id}/videos"


def get_videos_from_channel(channel_id: str, sleep: int = 1) -> List:
    """Crawl all videos in channel"""
    videos = []

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    response = session.get(channel_video_url(channel_id))
    html = response.text
    session_token = find_value(html, "XSRF_TOKEN", 3)

    data = json.loads(find_value(
        html, "window[\"ytInitialData\"] = ", 0, "\n").rstrip(";"))
    ncd = next(search_dict(data, "nextContinuationData"))
    continuations = [(ncd["continuation"], ncd["clickTrackingParams"])]

    while continuations:
        print("continue")
        continuation, itct = continuations.pop()
        response = ajax_request(session, YOUTUBE_VIDEOS_AJAX_URL,
                                params={"action_get_comments": 1,  # Delete
                                        "pbj": 1,
                                        "ctoken": continuation,
                                        "continuation": continuation,
                                        "itct": itct},
                                data={"session_token": session_token},
                                headers={"X-YouTube-Client-Name": "1",
                                         "X-YouTube-Client-Version": "2.20200207.03.01"})

        if not response:
            break
        if list(search_dict(response, "externalErrorMessage")):
            raise RuntimeError("Error returned from server: " +
                               next(search_dict(response, "externalErrorMessage")))

        # Ordering matters. The newest continuations should go first.
        continuations = [(ncd["continuation"], ncd["clickTrackingParams"])
                         for ncd in search_dict(response, "nextContinuationData")] + continuations

        for video in search_dict(response, 'gridVideoRenderer'):
            data = {'video_id': video['videoId'],
                    "title": video["title"]["simpleText"],
                    "viewCount": video["viewCountText"]["simpleText"],
                    "thumbnail": video["thumbnail"]["thumbnails"][0]
                    }
            videos.append(data)

        time.sleep(sleep)
    return videos
