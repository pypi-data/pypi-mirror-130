import datetime
import re
from urllib import parse

import requests
from bs4 import BeautifulSoup

URL_CALENDAR = "https://innherredrenovasjon.no/tommeplan/{premise_id}/kalender/"
URL_ADDRESS_SEARCH = "https://innherredrenovasjon.no/wp-json/ir/v1/addresses/{}"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Cache-Control": "max-age=0",
}


def find_address(address: str) -> dict[str, str]:
    result = requests.get(URL_ADDRESS_SEARCH.format(parse.quote(address)), headers=DEFAULT_HEADERS).json()
    return dict((e['id'], e['address']) for e in result['data']['results'])


def get_calendar(premise_id: str):
    response = requests.get(URL_CALENDAR.format(premise_id=premise_id), headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    year = int(re.findall(r"\d{4}", soup.find('h2', class_='article__title').get_text(strip=True)).pop())
    items = []
    types = []
    for item in soup.findAll('div', class_='gd-calendar__list-item'):
        datestr = re.findall(r"(\d{2})\.(\d{2})",
                             item.find(class_='gd-calendar__list-item-date').get_text(strip=True)).pop()
        dt_format = datetime.datetime.strptime(f"{year}-{datestr[1]}-{datestr[0]}", "%Y-%m-%d")
        entry = {
            "date": dt_format,
            "type": item.find(class_='gd-calendar__list-item-type').get_text(strip=True),
        }

        if entry['type'] not in types:
            types.append(entry['type'])
        items.append(entry)

    return items


def get_next_pickup(premise_id: str):
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    n = []
    for e in get_calendar(premise_id):
        if (e['date'] > today and len(n) == 0) or (len(n) > 0 and n[0]['date'] == e['date']):
            n.append(e)

    if len(n) == 0:
        return None

    return {
        "date": n[0]['date'],
        "types": " + ".join([e['type'] for e in n]),
    }
