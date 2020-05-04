import json

from ycd import downloader, simple_downloader
from ycd.simple_downloader import search_comments, get_comments_from_data

from logger import logger
from videos import get_videos_from_channel


ret = []
errors = []
failed = []

for channel_id, channel_title in [("UCIYNYv9ddZBg42gvyp8L2Iw", "팀브라더스"), ("UCIB_oNqi62rKnPFb3Toaozw", "코리안브로스"), ("UC270ueFEsQ21S26TYI_9yVA", "야신야덕")]:
    logger.info(f"Crawling videos from : {channel_title}")

    videos = get_videos_from_channel(channel_id)

    for video in videos:
        logger.info(f"Crawling comments from : {video['title']}")
        try:
            comments = search_comments(video["video_id"])
            cleaned_comments = get_comments_from_data(comments)
            video.update({
                "comments": comments,
                "cleaned_comments": cleaned_comments,
            })
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            logger.error(e)
            errors.append(video)

    ret.append({"channel_title": channel_title, "videos": videos})


for video in errors:
    try:
        comments = search_comments(video["video_id"])
        cleaned_comments = get_comments_from_data(comments)
        video.update({
            "video_publish_date": str(video["video_publish_date"]),
            "collection_date": str(video["collection_date"]),
            "comments": comments,
            "cleaned_comments": cleaned_comments,
        })
    except:
        failed.append(video)

data = {"success": ret, "errors": errors, "failed": failed}

with open("/tmp/yt.json", "w") as fp:
    json.dump(data, fp, ensure_ascii=False)
