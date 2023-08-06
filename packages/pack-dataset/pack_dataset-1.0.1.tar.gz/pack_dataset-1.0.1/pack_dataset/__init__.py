from pack_dataset.dataset_loader import GetterData


def create_connect(username=None, password=None):
    if (type(username) == str) and (type(password) == str):
        return GetterData(username, password)
    else:
        print('Создайте пожалуйста подключение указав свой корректный логин и пароль!')
