import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

r = requests.get('https://ani.gamer.com.tw/', headers=headers)
# r = <Response [200]>
if r.status_code == 200:
    print(f'請求成功：{r.status_code}')

    soup = BeautifulSoup(r.text, 'html.parser')
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
        anime_href = anime_item.select_one('a.anime-card-block').get('href')
        print("動畫網址 : ", 'https://ani.gamer.com.tw/'+anime_href)

        print('----------')

        images = anime_item.select_one('.anime-blocker').findAll('img')[0]
        print(images['src'])

else:
    print(f'請求失敗：{r.status_code}')
