import re
import datetime
from dataclasses import dataclass
from typing import Iterable

import requests
from bs4 import BeautifulSoup

TODAY = datetime.date.today()
DAYS_OF_A_WEEK = 7


@dataclass
class MenuCard:
    time: str
    menu: Iterable[str]
    date: datetime.date

    def check_date(self, date: datetime.date):
        return self.date == date


def check_weekend(date: datetime.date):
    return date.isoweekday() > 5


def extract_menu(section) -> MenuCard:
    time = section.find("strong", class_="cm_date").get_text().strip()
    month, day = map(int, re.findall("[0-9]{1,2}", time))
    date = datetime.date(TODAY.year, month, day)
    menu = section.find("div", class_="time_normal_list").find_all(
        "span", class_="text"
    )
    menu = [dish.get_text() for dish in menu]

    return MenuCard(time, menu, date)


def scrape_menu() -> Iterable[MenuCard]:
    menu_cards: Iterable[MenuCard] = []
    url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blBI&pkid=682&os=24929782&qvt=0&query=%EB%8C%80%EA%B1%B4%EA%B3%A0%EB%93%B1%ED%95%99%EA%B5%90%20%EA%B8%89%EC%8B%9D%EC%8B%9D%EB%8B%A8"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "lxml")

    target_date = (
        TODAY
        if not check_weekend(TODAY)
        else TODAY + datetime.timedelta(days=DAYS_OF_A_WEEK - TODAY.weekday())
    )
    _, curr_week, next_week = soup.find_all("div", class_="timeline_list")
    target_week = curr_week if not check_weekend(TODAY) else next_week
    sections = target_week.find_all("div", class_="timeline_box")
    for section in sections:
        extracted_menu = extract_menu(section)
        if extracted_menu.check_date(target_date):
            menu_cards.append(extracted_menu)

    return menu_cards
