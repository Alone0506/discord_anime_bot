from collections import defaultdict


class Handle_follow_info():
    def __init__(self):
        self.info_dict = defaultdict(list)

    def txt_to_dict(self):
        with open('follow_info.txt', 'r', encoding="utf-8") as f:
            infos = f.readlines()

            for info in infos:
                user_name = info.strip().split(" ", 2)[0]
                episode = info.strip().split(" ", 2)[1]
                anime_name = info.strip().split(" ", 2)[2]
                self.info_dict[user_name].append([episode, anime_name])

        f.close()

    def dict_to_txt(self, user_name, episode, anime_name):
        with open('follow_info.txt', 'a', encoding="utf-8") as f:
            f.write(f"{user_name} {episode} {anime_name}\n")
        f.close()

    def isnew_user(self, user_name):
        self.txt_to_dict()
        if str(user_name).strip() not in self.info_dict:
            return True
        return False

    def isodd_user_follow(self, user_name, episode, anime_name):
        user_name = str(user_name).strip()
        if [episode, anime_name] in self.info_dict[user_name]:
            return True
        return False

    def add_follow_info_to_txt(self, user_name, episode, anime_name):
        self.info_dict[user_name].append([episode, anime_name])
        self.dict_to_txt(user_name, episode, anime_name)


# a = Handle_follow_info()
# if a.isnew_user('zOEe#0506'):
#     a.add_follow_info_to_txt('zOEe#0506', '第23集', 'BB')
# else:
#     if a.isodd_user_follow('zOEe#0506', '第23集', 'BB'):
#         pass
#     else:
#         a.add_follow_info_to_txt('zOEe#0506', '第23集', 'BB')
