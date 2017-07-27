import requests
from pytz import timezone
from datetime import datetime


def get_content_users(payload):
    url_based = 'https://devman.org/api/challenges/solution_attempts/'
    content = requests.get(url_based, params=payload)
    content_users = content.json()
    return content_users


def get_the_number_of_pages(content_users):
    the_number_of_pages = int(content_users['number_of_pages'])
    return the_number_of_pages


def get_users_info(content_users):
    for info_users in content_users['records']:
        yield {'username': info_users['username'],
               'timestamp': info_users['timestamp'],
               'timezone': info_users['timezone'],
               }


def get_users_info_from_the_first_page(content_users):
    return get_users_info(content_users)


def get_other_users_info(page_count, key_for_url):
    start_page = 2
    number_for_range = page_count + 1
    for number_page in range(start_page, number_for_range):
        payload = {key_for_url: number_page}
        content = get_content_users(payload)
        content_from_other_pages = get_users_info(content)
    return content_from_other_pages


def get_midnight_user(info_files):
    start_in_the_morning = 5
    time_zone = info_files['timezone']
    if info_files['timestamp']:
        time_devman = datetime.fromtimestamp(info_files['timestamp'])
        user_time = timezone(time_zone).fromutc(time_devman)
        return user_time.hour < start_in_the_morning


def get_set_users(content_user):
    set_users = set()
    for user_info in (content_user):
        if get_midnight_user(user_info):
            set_users.add(user_info['username'])
    return set_users


def show_information(content_from_the_first_page, content_from_other_pages):
    if get_set_users(content_from_the_first_page):
        all_users_info = get_set_users(content_from_other_pages).update(content_from_the_first_page)
    all_users_info = get_set_users(content_from_other_pages)
    return all_users_info


if __name__ == '__main__':
    number_page = 1
    key_for_url = 'page'
    payload = {key_for_url: number_page}
    content_users = get_content_users(payload)
    page_count = get_the_number_of_pages(content_users)
    content_from_the_first_page = get_users_info_from_the_first_page(content_users)
    content_from_other_pages = get_other_users_info(page_count, key_for_url)
    for content in content_from_other_pages:
        print(content)
    all_users_info = show_information(content_from_the_first_page,
                                      content_from_other_pages)
    print('Users are night owls:')
    for number, user in enumerate(all_users_info):
        print(number, user)
