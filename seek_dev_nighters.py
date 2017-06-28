import requests
from pytz import timezone
from datetime import datetime


def get_user_information():
    url_based = 'https://devman.org/api/challenges/solution_attempts/?page=1'
    content = requests.get(url_based)
    content_users = content.json()
    pages = int(content_users['number_of_pages'])

    for page in range(1, pages):
        url = 'http://devman.org/api/challenges/solution_attempts/?page={}'.format(page)
        content = requests.get(url)
        content = content.json()
        for content_users in content['records']:
            yield {'username': content_users['username'],
                   'timestamp': content_users['timestamp'],
                   'timezone': content_users['timezone'],
                  }


def get_midnight_user(info):
    time_zone = info['timezone']
    if info['timestamp']:
        time_devman = datetime.fromtimestamp(info['timestamp'])
        user_time = timezone(time_zone).fromutc(time_devman)
        return bool(user_time.hour < 5)


def get_set_users():
    content_user = get_user_information()
    set_users = set()
    for user_info in content_user:
        if get_midnight_user(user_info):
            set_users.add(user_info['username'])
    return set_users


if __name__ == '__main__':
    print(get_set_users())