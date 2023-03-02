from database.crud import DevCrud


async def get_dev_list(params=None):
    user_list = await DevCrud.get_devs()
    return list(user_list)


if __name__ == "__main__":
    print(get_dev_list())
