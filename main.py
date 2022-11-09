from fake_headers import Headers
import requests
from bs4 import BeautifulSoup
import re


def get_post_url(all_posts):
    links = []
    for post in all_posts:
        header = post.find('h2')
        a = header.find(class_="tm-article-snippet__title-link")
        links.append(a['href'])
    return links


def get_post_date(soup):
    post_date = soup.find('time')
    if post_date:
        return post_date['title']
    else:
        return 'Дата не найдена!'


def get_post_header(soup):
    post_header = soup.find('h1')
    if post_header:
        return post_header.find('span').text
    else:
        return 'Заголовок не найден!'


def search_for_keywords(post):
    for keyword in KEYWORDS:
        if re.search(keyword, post, re.IGNORECASE):
            return True


if '__main__' == __name__:
    KEYWORDS = ['интернет', 'IT', 'Python', 'статистика']
    start_url = 'https://habr.com'
    all_url = '/ru/all/'

    headers = Headers(browser='Chrome', os='win', headers=True).generate()
    response = requests.get(start_url+all_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('article')
    all_links = get_post_url(posts)

    for link in all_links:
        link_url = start_url+link
        response = requests.get(link_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        post = soup.find(id='post-content-body')
        post_text = post.text
        if search_for_keywords(post_text):
            post_header = get_post_header(soup)
            post_date = get_post_date(soup)
            print(f'{post_header}\n'
                  f'{post_date}\n'
                  f'{link_url}')

