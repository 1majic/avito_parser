import datetime
import urllib.parse
from collections import namedtuple

import bs4
import requests
import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute(f"select url from blocks")
alls = [''.join(i) for i in cursor.fetchall()]

InnerBlock = namedtuple('Block', 'title,price,currency,date,url')
new = []


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title},{self.price},{self.currency},{self.date},{self.url}'


class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Accept-Language': 'ru',
            'cookie': 'u=2oua41v6.q4kont.1a3e5zqlua400; abp=1; _gcl_au=1.1.753166676.1627890463; '
                      '_ym_uid=1614689243225712254; _ym_d=1627890465; isWideScreen=true; no-ssr=1; '
                      'buyer_local_priority_v2=1; SEARCH_HISTORY_IDS=4,; buyer_location_id=646520; '
                      'buyer_popup_location=646520; '
                      '__gads=ID=b33e361fea0f15dc:T=1627890816:S=ALNI_Mbxy1yyZ9SlumOA_zaSgl1KMe7ygQ; '
                      'luri=sterlitamak; _gid=GA1.2.1135837561.1628275114; '
                      'showedStoryIds=69-68-66-63-62-61-58-50-49-48-47-42-32; lastViewingTime=1628275115963; '
                      '_ym_isad=1; '
                      'st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                      '.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRWJyOTgwNUlPUUZVNFZnQXBMQTJ6VHk2bVRLRlA5Ym5jc1VTUzFwYS9EazJCRkNjRGt4QVRmZnVHNExHWnZZUzhtSGNRYmlCSFRzTHlwOHVsb2l4ZVdWNlpzdUw3S3pCeHlPVkVVeHorN2R5M3h2Z1RYRFgrUk1GWkJma2ZLQ25DclJya0R6NCtNemx4bTYvTEVQMTIzZ0p0Z2Y1NFdtb0NGWFBrOFlTQ0FoKzJIVlZFSVNGUFZxc1RnMllZbFRJa3FFMjRyeWZpeW15NkxFd3NCd3hEOC9SNVZUYm5zVHJMaTZGSTZ6OUxjWmZ6SkdobjFkUjVOOFBXbFplMXFsNGQiLCJpYXQiOjE2Mjc4OTA0ODQsImV4cCI6MTYyOTEwMDA4NH0.7ESHoJbUulDZQWVV1D0Mvel-CD18NRzGC5-AJ9SYSeQ; f=5.32e32548b6f3e978cc0065cb1b69001fe404c9a8ad2fd516e404c9a8ad2fd516e404c9a8ad2fd516e404c9a8ad2fd516d8b16176e03d2873d8b16176e03d2873d8b16176e03d2873e404c9a8ad2fd5160da5ab2fc5c813503d6c212bc3ab3fc346b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e92157fc552fc06411bc8794f0f6ce82fe915ac1de0d034112dc0d86d9e44006d8143114829cf33ca7143114829cf33ca724a135baa76198de46b8ae4e81acb9fad99271d186dc1cd0b5b87f59517a23f2c772035eab81f5e1c772035eab81f5e13de19da9ed218fe2c772035eab81f5e1143114829cf33ca7b586f2e2c69f69666eaa185079056ac700d08494bf8df9c2a93953dab92cf7eb488d323de47b4cc85e61d702b2ac73f7f90229014725d11961a46dbbf9840d472af9e5c04fd1603fb211361d778c31aa1cf5fc67cf4c79a90df103df0c26013a0df103df0c26013aafbc9dcfc006bed99c9a80bc42477af7a572f99f6f9fd2eb3de19da9ed218fe23de19da9ed218fe2d6fdecb021a45a31b3d22f8710f7c4ed78a492ecab7d2b7f; ft="gQWsUjppGl+tmDnSf37q9LfuyqcNrmslrsUAzwBC62vyo9HACxF0tIHKHREvGgKC5lxfdSXLi+ru9FBGnUzAf2wf8jkIxcZhvLWUtoWyEmQTnJnuYcBuLURAnBQO81oKH3jqUAEI4A1kOgar+cdgwtmMXtF0AGWW+l5ov7NUmeOZ6Nw0VSMoTXNJABmEKUw2"; v=1628277051; _ym_visorc=b; dfp_group=28; sx=H4sIAAAAAAACA1XRQXLCMAwF0Lt4zUJJFFtwm0QFNTggOiIRA8PdKxZ0ildefD/7W4/UH9blfu1uc+OM5lLNgAzY0u6R1rRLvOKlXcZLOTC7C2AFFDFQNlXTtEn7tGtyS11ueqDnJnWnaR0sUiDgyKzVq7MDvUkcf/x6mx1HQ0ON+8ikKlQhQ66f5LYNcj5P216P7XVSQyIBJrPYvUU6dwMc6HSrJkwiXE0rVYdY7J9i7nKI49yWoR0lNw5OogqIcYTkTU5anPL5UibBaIFs0V0J1BHM5PORBYP8Gn702DTZiZRMo3+0i+gfaUtZSi51H3da9H0lXmFhFzf6JHsIcjjdy2GdWyvG5sQxHFFU0TdZ+uY775vb8cyONcbHURsYhRjiK/6T2G23z+cvUofuJPIBAAA=; so=1628277999; _ga_9E363E7BES=GS1.1.1628277047.3.1.1628278002.60; _ga=GA1.1.1449825270.1627890464; _dc_gtm_UA-2546784-1=1',
            'referer': 'https://www.avito.ru/sterlitamak/odezhda_obuv_aksessuary',
            'sec - ch - ua': '"Not A;Brand"; v = "99", "Chromium"; v = "90"',
            'sec - ch - ua - mobile': '?0',
            'sec - fetch - dest': 'document',
            'sec - fetch - mode': 'navigate',
            'sec - fetch - site': 'same - origin',
            'sec - fetch - user': '?1',
            'upgrade - insecure - requests': '1',
            'user - agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.222 Safari/537.36'
        }

    def get_page(self, page: int = None, search: str = None):
        params = {
            'radius': 0,
            'user': 1,
            'q': search
        }
        if page and page > 1:
            params['p'] = page

        url = 'https://www.avito.ru/sterlitamak/oborudovanie_dlya_biznesa?geoCoords=53.630403%2C55.930825&q=asic&radius=50'
        # r = self.session.get(url, params=params)
        r = self.session.get(url)
        return r.text

    @staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')
        # print(params)
        if len(params) == 3:
            left, types = int(params[0]), ' '.join(params[1:]).lower()
            if types == 'минут назад':
                date = datetime.date.today() - datetime.timedelta(minutes=left)
            elif types == 'часов назад':
                date = datetime.date.today() - datetime.timedelta(hours=left)
            elif types == 'дня назад':
                date = datetime.date.today() - datetime.timedelta(days=left)
            elif types == 'недели назад':
                date = datetime.date.today() - datetime.timedelta(weeks=left)
            else:
                date = ' '.join(params[:1])
                return date

            # elif len(params) == 3:
            month_hru = date.month
            months_map = {
                'января': 1,
                'февраля': 2,
                'марта': 3,
                'апреля': 4,
                'мая': 5,
                'июня': 6,
                'июля': 7,
                'августа': 8,
                'сентября': 9,
                'октября': 10,
                'ноября': 11,
                'декабря': 12,
            }
            # month = months_map.get(month_hru)
            # if not month:
            #     print('Не смогли разобрать месяц:', item)
            #     return
            #
            # today = datetime.datetime.today()
            # time = datetime.datetime.strptime(time, '%H:%M')
            return datetime.datetime(day=date.day, month=date.month, year=date.year)
        else:
            print('Не смогли разобрать формат:', item)
            return

    def parse_block(self, item):
        # Выбрать блок со ссылкой
        url_block = item.select_one(
            'a.link-link-39EVK.link-design-default-2sPEv.title-root-395AQ.iva-item-title-1Rmmj.title-listRedesign-3RaU2.title-root_maxHeight-3obWc')
        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        # Выбрать блок с названием
        title_block = item.select_one(
            'h3.title-root-395AQ.iva-item-title-1Rmmj.title-listRedesign-3RaU2.title-root_maxHeight-3obWc.text-text-1PdBw.text-size-s-1PUdo.text-bold-3R9dt')
        title = title_block.string.strip()

        # Выбрать блок с названием и валютой
        price_block = item.select_one('span.price-text-1HrJ_.text-text-1PdBw.text-size-s-1PUdo')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block) == 2:
            price, currency = price_block
        elif len(price_block) == 1:
            # Бесплатно
            price, currency = 0, None
        else:
            price, currency = None, None
            print(f'Что-то пошло не так при поиске цены: {price_block}, {url}')

        # Выбрать блок с датой размещения объявления
        date = None
        date_block = item.select_one('div.date-text-2jSvU.text-text-1PdBw.text-size-s-1PUdo.text-color-noaccent-bzEdI')
        absolute_date = date_block.text
        # if absolute_date:
        #     date = self.parse_date(item=absolute_date)
        date = absolute_date

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=date,
        )

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('a.pagination-page')
        try:
            last_button = container[-1]
            href = last_button.get('href')
            if not href:
                return 1

            r = urllib.parse.urlparse(href)
            params = urllib.parse.parse_qs(r.query)
            return int(params['p'][0])
        except:
            return len(soup.find('div.pagination-root-2oCjZ').find_all('span'))

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # Запрос CSS-селектора, состоящего из множества классов, производится через select
        container = soup.select('div.iva-item-root-G3n7v.photo-slider-slider-3tEix.iva-item-list-2_PpT.iva-item'
                                '-redesign-1OBTh.items-item-1Hoqq.items-listItem-11orH.js-catalog-item-enum')
        for item in container:
            block = self.parse_block(item=item)
            if block.url not in alls and block is not None:
                print(f'Новый элемент\n{block}\n\n')
                cursor.execute(f"INSERT INTO blocks"
                               f"(title, price, date, url)"
                               f"VALUES ('{block.title}','{block.price}', '{block.date}','{block.url}');")
                new.append(block)
                conn.commit()
                print(f'{block.title}', f'{block.price}', f'{block.date}', f'{block.url}')

    def parse_all(self):
        # limit = self.get_pagination_limit()
        limit = 5
        print(f'Всего страниц: {limit}')

        # limit1 = int(input('Укажите количество страниц для парсинга: '))
        limit1 = 1
        if limit1 < limit:
            limit = 1
        elif limit > limit1 > 1:
            limit = limit1

        for i in range(1, limit + 1):
            self.get_blocks(page=i)


def main():
    global conn, cursor, alls
    p = AvitoParser()
    p.parse_all()
    return new


if __name__ == '__main__':
    main()
