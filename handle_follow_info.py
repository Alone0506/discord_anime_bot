class Handle_follow_info():
    def __init__(self):
        pass

    def check_follow(self, user, episode, anime_name):
        f = open('follow_info.txt', 'w+')
        if f.readlines():
            print(user, episode, anime_name)
