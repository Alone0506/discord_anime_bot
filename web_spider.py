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
            self.newanime_item = self.soup.select_one(
                '.timeline-ver > .newanime-block')
            self.anime_items = self.newanime_item.select(
                '.newanime-date-area:not(.premium-block)')

        self.anime_name_list = []
        self.anime_watch_number_list = []
        self.anime_episode_list = []
        self.anime_href_list = []
        self.anime_picture_list = []

    def anime_info(self):
        if self.r.status_code == 200:
            for anime_item in self.anime_items:

                name = anime_item.select_one('.anime-name > p').text.strip()
                self.anime_name_list.append(name)

                watch_number = anime_item.select_one(
                    '.anime-watch-number > p').text.strip()
                self.anime_watch_number_list.append(watch_number)

                if anime_item.select_one('.anime-episode').text.strip():
                    episode = anime_item.select_one(
                        '.anime-episode').text.strip()
                    self.anime_episode_list.append(episode)
                else:
                    self.anime_episode_list.append("OVA")

                href = anime_item.select_one('a.anime-card-block').get('href')
                self.anime_href_list.append('https://ani.gamer.com.tw/' + href)

                picture = anime_item.select_one(
                    '.anime-blocker').findAll('img')[0]
                self.anime_picture_list.append(picture['src'])

            return [self.anime_name_list, self.anime_watch_number_list, self.anime_episode_list, self.anime_href_list, self.anime_picture_list]

        else:
            return self.r.status_code


a = Anime().anime_info()
print(a)
