import requests
from pytz import timezone
from datetime import datetime


def get_the_number_of_pages():
    url_based = 'https://devman.org/api/challenges/solution_attempts/?page=1'
    content = requests.get(url_based)
    content_users = content.json()
    the_number_of_pages = int(content_users['number_of_pages'])
    return the_number_of_pages, content_users


def get_users_info_from_the_first_page(content_users):
    for info_users in content_users['records']:
        yield {'username': info_users['username'],
               'timestamp': info_users['timestamp'],
               'timezone': info_users['timezone'],
               }

def get_users_info(page_count):
    start_page = 2
    for page in range(start_page, page_count):
        url = 'http://devman.org/api/challenges/solution_attempts/?page={}'.format(page)
        content = requests.get(url)
        content = content.json()

        for info_users in content['records']:
            yield {'username': info_users['username'],
                   'timestamp': info_users['timestamp'],
                   'timezone': info_users['timezone'],
                  }


def get_midnight_user(info):
    start_in_the_morning = 5
    time_zone = info['timezone']
    if info['timestamp']:
        time_devman = datetime.fromtimestamp(info['timestamp'])
        user_time = timezone(time_zone).fromutc(time_devman)
        return user_time.hour < start_in_the_morning


def get_set_users(content_user):
    set_users = set()
    for user_info in content_user:
        if get_midnight_user(user_info):
            set_users.add(user_info['username'])
    return set_users


def show_information():
    if get_set_users(content_from_the_first_page):
        all_users_info = get_set_users(content_from_other_pages).update(content_from_the_first_page)
    all_users_info = get_set_users(content_from_other_pages)
    print('Users are night owls:')
    for number, user in enumerate(all_users_info):
        print(number, user)

if __name__ == '__main__':
    page_count, content = get_the_number_of_pages()
    content_from_the_first_page = get_users_info_from_the_first_page(content)
    content_from_other_pages = get_users_info(page_count)
    show_information()
