def write_file(user, episode, anime_name):
    with open('follow_info.txt', 'a+', encoding="utf-8") as f:
        # 'a+' 模式下 游標預設會再最後面
        f.seek(0)
        info = f.readlines()

        if info == []:
            print(info)
            f.write(f"{user} {episode} {anime_name}")
            f.write("\n")
        else:
            print(info, "aaaaaaaaaaaa")
        f.close()


write_file("Alone#0506", "第24集", "Mumei Love Me")
