import os
from dataclasses import dataclass
from typing import Iterable, Union

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
USER_AGENT = os.getenv('USER_AGENT')

@dataclass(kw_only=True, frozen=True)
class News:
    title: str
    url: str
    summary: str
    press: str
    thumbnail: str

def extract_news(content) -> Union[News, None]:
    try:
        headline = content.find('a', class_='cluster_text_headline')
        title = headline.get_text()
        url = headline['href']
        summary = content.find('div', class_='cluster_text_lede').get_text()
        press = content.find('div', class_='cluster_text_press').get_text()
        thumbnail = content.find('a', class_='cluster_thumb_link').find('img')['src']
    except AttributeError:
        return
    return News(
        title=title,
        url=url,
        summary=summary,
        press=press,
        thumbnail=thumbnail
    )

def scrape_news() -> Iterable[News]:
    news_list: Iterable[News] = []
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"
    headers = {'User-Agent': USER_AGENT}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'lxml')

    sections = soup.find_all('div', class_='cluster_group')
    for section in sections:
        contents = section.find_all('li', class_='cluster_item')
        for content in contents:
            extracted_news = extract_news(content)
            if isinstance(extracted_news, News):
                news_list.append(extracted_news)

    return news_list

if __name__ == "__main__":
    news_list = scrape_news()
    for news in news_list:
        print(news)