import requests
from pytz import timezone
from datetime import datetime


def get_content_with_info_about_users(payload):
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


def get_info_about_all_users(page_count, key_for_url, content_with_first_page):
    start_page = 2
    number_for_range = page_count + 1
    for number_page in range(start_page, number_for_range):
        payload = {key_for_url: number_page}
        content = get_content_with_info_about_users(payload)
        info_about_users = get_users_info(content)
        info_about_users_first_page = get_users_info(content_with_first_page)
    return info_about_users, info_about_users_first_page


def get_users_night_owls(info_files):
    start_in_the_morning = 5
    time_zone = info_files['timezone']
    if info_files['timestamp']:
        time_devman = datetime.fromtimestamp(info_files['timestamp'])
        user_time = timezone(time_zone).fromutc(time_devman)
        return user_time.hour < start_in_the_morning


def get_set_midnights_users(content_user):
    set_users = set()
    for user_info in (content_user):
        if get_users_night_owls(user_info):
            set_users.add(user_info['username'])
    return set_users


def show_information(info_about_all_users):
    clear_info_about_users = get_set_midnights_users(info_about_all_users)
    return clear_info_about_users


if __name__ == '__main__':
    number_page = 1
    key_for_url = 'page'
    payload = {key_for_url: number_page}
    content_with_first_page = get_content_with_info_about_users(payload)
    page_count = get_the_number_of_pages(content_with_first_page)
    info_about_users, info_with_first_page = get_info_about_all_users(page_count, key_for_url, content_with_first_page)
    if show_information(info_with_first_page):
        clear_info_about_users = show_information(info_about_users).update(show_information(info_with_first_page))
    clear_info_about_users = show_information(info_about_users)
    if clear_info_about_users:
        print('Users are night owls:')
        for number, user in enumerate(clear_info_about_users):
            print(number, user)
    else:
        print('All users sleep at night!')
