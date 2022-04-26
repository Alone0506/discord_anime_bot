import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}


class Anime:
    def __init__(self):
        self.r = requests.get('https://ani.gamer.com.tw/', headers=headers)
        if self.r.status_code == 200:
            self.soup = BeautifulSoup(self.r.text, 'html.parser')

            # 依更新日排的新番列表
            self.newanime_block = self.soup.select_one(
                '.timeline-ver > .newanime-block')
            # 每一格新番
            self.anime_items = self.newanime_block.select(
                '.newanime-date-area:not(.premium-block)')

            self.program_list = self.soup.select('.programlist-block')

    def newanime_info(self):

        return_dict = {}
        if self.r.status_code == 200:
            for anime_item in self.anime_items:
                tmp_dict = {}
                # 動畫名稱
                name = anime_item.select_one('.anime-name > p').text.strip()
                # 觀看次數
                watch_number = anime_item.select_one(
                    '.anime-watch-number > p').text.strip()
                # 最新集數
                if anime_item.select_one('.anime-episode').text.strip():
                    episode = anime_item.select_one(
                        '.anime-episode').text.strip()
                else:
                    episode = "此為OVA或電影"
                # 動畫網址
                href = anime_item.select_one('a.anime-card-block').get('href')
                href = 'https://ani.gamer.com.tw/' + href
                # 動畫縮圖
                picture = anime_item.select_one(
                    '.anime-blocker').findAll('img')[0]
                picture = picture['src']
                # 更新時間
                update_hour = anime_item.find_all(
                    'span', class_='anime-hours')[0]
                update_hour = list(update_hour)
                update_day = anime_item.find_all(
                    'span', class_='anime-date-info anime-date-info-block-arrow')[0]
                update_day = list(update_day)
                if update_day[-1].strip() == "其他":
                    update_time = "其他"
                else:
                    update_time = update_day[-1].strip() + \
                        update_hour[0].strip()

                tmp_dict[name] = [watch_number,
                                  episode, update_time, href, picture]

                return_dict.update(tmp_dict)

            return return_dict

        else:
            return self.r.status_code

    def renew(self):
        return_dict = {}
        if self.r.status_code == 200:
            day_list = self.soup.select('.day-list')
            for anime_block in day_list:
                tmp_dict = {}
                anime_info_list = []

                day_title = anime_block.select_one('h3').get_text().strip()

                if anime_block.select('.text-anime-info') != []:
                    for i in anime_block.select('.text-anime-info'):

                        anime_name = i.select_one('.text-anime-name')
                        anime_name = anime_name.get_text().strip()

                        anime_time = i.select_one('.text-anime-time')
                        anime_time = anime_time.get_text().strip()

                        anime_episode = i.select_one('.text-anime-number')
                        anime_episode = anime_episode.get_text().strip()

                        anime_info_list.append(
                            [anime_name, anime_time, anime_episode])

                else:
                    text = anime_block.select_one('.pic-no-content')
                    text = text.get_text().strip()

                    image = anime_block.select_one(
                        '.pic-no-content').find('img')
                    image = image['src']

                    anime_info_list.append([text, image])

                tmp_dict[day_title] = anime_info_list

                return_dict.update(tmp_dict)

        return return_dict


# a = Anime().newanime_info()
# print(a)
