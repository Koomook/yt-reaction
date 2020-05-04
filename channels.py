from typing import Dict, List

from bs4 import BeautifulSoup as BS
import requests

def channel_list_url_page(page: int) -> str:
    return f"https://www.youha.info/search/channel/?q=&order=&category_id=&subscriber_over=&email=&mcn=&period=&page={page}"

def get_channels(max_page: int = 2000) -> List[Dict]:
    channels = []
    for page in range(1, max_page+1):
        url = channel_list_url_page(page)
        ret = requests.get(url)

        bs = BS(ret.text, "lxml")

        for data in bs.select("td .hidden-for-mobile"):
            _channel_char, channel_id = data.attrs["href"].strip("/").split("/")
            assert _channel_char == "channel"
            channels.append({"id": channel_id, "name": data.text})

    return channels
