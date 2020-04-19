from typing import Dict

from youtube_api import YouTubeDataAPI


class YoutubeCommentAnalyzer(YouTubeDataAPI):
    
    def __init__(self, key, **kwargs) -> None:
        super().__init__(key, **kwargs)
    
    def get_comments_from_channel(self, channel_id: str) -> Dict:
        videos = self.search(channel_id=channel_id, max_results=1000)
        
        for i, video in enumerate(videos):
            comments = self.get_video_comments(video_id=video["video_id"])
            video.update(
                {
                    "link": f"https://www.youtube.com/watch?v={video['video_id']}",
                    "comments": comments,
                })
            if (i+1) % 10 == 0:
                print(f"{i}th video done")
        self.videos_from_channel = {"videos": videos, "channel_id": channel_id}
        return videos
