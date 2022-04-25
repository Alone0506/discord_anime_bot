import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
print("a")


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

        anime_name_list = []
        anime_watch_number_list = []
        anime_episode_list = []
        anime_href_list = []
        anime_image_list = []
        anime_update_time_list = []

        if self.r.status_code == 200:
            for anime_item in self.anime_items:
                # 動畫名稱
                name = anime_item.select_one('.anime-name > p').text.strip()
                anime_name_list.append(name)
                # 觀看次數
                watch_number = anime_item.select_one(
                    '.anime-watch-number > p').text.strip()
                anime_watch_number_list.append(watch_number)
                # 最新集數
                if anime_item.select_one('.anime-episode').text.strip():
                    episode = anime_item.select_one(
                        '.anime-episode').text.strip()
                    anime_episode_list.append(episode)
                else:
                    anime_episode_list.append("此為OVA或電影")
                # 動畫網址
                href = anime_item.select_one('a.anime-card-block').get('href')
                anime_href_list.append('https://ani.gamer.com.tw/' + href)
                # 動畫縮圖
                picture = anime_item.select_one(
                    '.anime-blocker').findAll('img')[0]
                anime_image_list.append(picture['src'])
                # 更新時間
                update_hour = anime_item.find_all(
                    'span', class_='anime-hours')[0]
                update_hour = list(update_hour)
                update_day = anime_item.find_all(
                    'span', class_='anime-date-info anime-date-info-block-arrow')[0]
                update_day = list(update_day)
                if update_day[-1].strip() == "其他":
                    anime_update_time_list.append("僅有一集")
                else:
                    anime_update_time_list.append(
                        update_day[-1].strip() + update_hour[0].strip())

            return [anime_name_list, anime_watch_number_list, anime_episode_list, anime_update_time_list, anime_href_list, anime_image_list]

        else:
            return self.r.status_code

    def newanime_info(self):

        if self.r.status_code == 200:
            for day_list in self.program_list:
                print(day_list)
