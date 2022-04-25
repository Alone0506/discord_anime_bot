import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

r = requests.get('https://ani.gamer.com.tw/', headers=headers)
# r = <Response [200]>
soup = BeautifulSoup(r.text, 'html.parser')


def newanime_info():
    if r.status_code == 200:
        print(f'請求成功：{r.status_code}')
        newanime_item = soup.select_one('.timeline-ver > .newanime-block')

        anime_items = newanime_item.select(
            '.newanime-date-area:not(.premium-block)')

        # 依序針對每個動畫區塊擷取資料
        for anime_item in anime_items:
            anime_name = anime_item.select_one('.anime-name > p').text.strip()
            print("動畫名稱 : ", anime_name)
            anime_watch_number = anime_item.select_one(
                '.anime-watch-number > p').text.strip()
            print("觀看次數 : ", anime_watch_number)
            try:
                anime_episode = anime_item.select_one(
                    '.anime-episode').text.strip()
                print("最新集數 : ", anime_episode)
            except:
                pass
            anime_href = anime_item.select_one(
                'a.anime-card-block').get('href')
            print("動畫網址 : ", 'https://ani.gamer.com.tw/'+anime_href)

            images = anime_item.select_one('.anime-blocker').findAll('img')[0]
            print("縮圖網址 : ", images['src'])

            update_hour = anime_item.find_all('span', class_='anime-hours')[0]
            update_hour = list(update_hour)
            print("更新時間 : ", update_hour[0].strip())
            update_day = anime_item.find_all(
                'span', class_='anime-date-info anime-date-info-block-arrow')[0]
            update_day = list(update_day)
            print("更新日期 : ", update_day[-1].strip())

            print('----------')

    else:
        print(f'請求失敗：{r.status_code}')


def renew():
    return_dict = {}
    if r.status_code == 200:
        day_list = soup.select('.day-list')
        for anime_block in day_list:
            tmp_dict = {}
            anime_info_list = []

            day_title = anime_block.select_one('h3').get_text().strip()

            if anime_block.select('.text-anime-info') != []:
                for i in anime_block.select('.text-anime-info'):

                    anime_time = i.select_one('.text-anime-time')
                    anime_time = anime_time.get_text().strip()

                    anime_name = i.select_one('.text-anime-name')
                    anime_name = anime_name.get_text().strip()

                    anime_episode = i.select_one('.text-anime-number')
                    anime_episode = anime_episode.get_text().strip()

                    anime_info_list.append(
                        [anime_time, anime_name, anime_episode])

            else:
                text = anime_block.select_one('.pic-no-content')
                text = text.get_text().strip()

                image = anime_block.select_one('.pic-no-content').find('img')
                image = image['src']

                anime_info_list.append([text, image])

            tmp_dict[day_title] = anime_info_list

            return_dict.update(tmp_dict)

    return return_dict


print(renew())
