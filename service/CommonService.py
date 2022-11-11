from config.Config import USER_LIST


def user_check(user: str, pwd: str) -> bool:
    flag = False
    for i in USER_LIST:
        pw = i.get(user)
        if pw == pwd:
            flag = True
    return flag


if __name__ == '__main__':
    print(user_check("admin", "admin"))
