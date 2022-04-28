from collections import defaultdict


class Handle_sub_info():
    def __init__(self):
        self.info_dict = defaultdict(list)

    def txt_to_dict(self):
        with open('sub_info.txt', 'r', encoding="utf-8") as f:
            infos = f.readlines()

            for info in infos:
                user_id = info.strip().split(" ", 2)[0]
                episode = info.strip().split(" ", 2)[1]
                anime_name = info.strip().split(" ", 2)[2]
                self.info_dict[user_id].append([episode, anime_name])

        f.close()

    def dict_to_txt(self, _dict: dict):
        with open('sub_info.txt', 'w+', encoding="utf-8") as f:
            f.read()
            f.seek(0)
            f.truncate(0)
            for user_id in _dict:
                for episode, anime_name in _dict[user_id]:
                    f.write(f"{user_id} {episode} {anime_name}\n")
        f.close()

    def issub(self, user_id: str, episode: str, anime_name: str):
        self.txt_to_dict()
        if user_id in self.info_dict and [episode, anime_name] in self.info_dict[user_id]:
            return True
        return False

# a = Handle_sub_info()
# if a.isnew_user('432431174397198339'):
#     a.info_dict['432431174397198339'].append(["第5集", "bulibuli"])
#     a.dict_to_txt(a.info_dict)
# else:
#     if a.isodd_user_sub('432431174397198339', "第5集", 'bulibuli'):
#         pass
#     else:
#         a.info_dict['432431174397198339'].append(["第5集", "bulibuli"])
#         a.dict_to_txt(a.info_dict)
