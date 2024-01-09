import requests


def get_cute_link(link):
    return requests.post('http://127.0.0.1:5000/create_cute_link', data={'link': link})


def link_exists(link):
    return requests.get(f'http://127.0.0.1:5000/{link}')


print(get_cute_link('https://google.com').text)
print(link_exists('f20b5bcd4c'))
