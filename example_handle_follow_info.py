def check_new_user(user, episode, anime_name):
    info_dict = {}
    with open('follow_info.txt', 'a+', encoding="utf-8") as f:
        # 'a+' 模式下 游標預設會再最後面
        f.seek(0)
        infos = f.readlines()

        if infos == []:
            print(infos)
            f.write(f"{user} {episode} {anime_name}\n")
        else:
            for info in infos:
                user_name = info.strip().split(" ", 2)[0]
                episode = info.strip().split(" ", 2)[1]
                anime_name = info.strip().split(" ", 2)[2]
                if user_name not in info_dict:
                    info_dict[user_name] = [[episode, anime_name]]
                else:

                    print(info_dict)
                    print(info_dict[user_name].append([1, 2]))
            print(info_dict)
        f.close()


def check_is_follow():
    pass


check_new_user("Alone#0506", "第24集", "Mumei Love Me")
check_new_user("Zeo", "第2集", "我的輝夜 大小姐")
