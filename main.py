import heapq
import re

import nltk
# from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup

from utils import (has_numbers, overwrite_file, remove_dupl_pres_order,
                   unique_lines_as_list, unique_lines_as_string)


def extract_html_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    page = requests.get(url, headers=headers)
    parsed_article = BeautifulSoup(page.text, 'lxml')
    return parsed_article

def extract_content_by_url(url, extract_by_numbers_only=False, punc_in_first_three_chars=True, filename='data_grab'):
    # punc_in_first_three_chars=True can only be run when extract_by_numbers_only=True

    # # TODO Address and understand headers requirements of requests.
    parsed_article = extract_html_from_url(url)
    body = parsed_article.find('body')
    body_string = body.prettify()

    # replace heading tags with coded paragraphs, so we can later identify heading level in text extracted / order of heading to paragraph.
    # heading start
    regex_text_clean = re.sub(r'<h1.{0,}', '<p>*<', body_string)
    regex_text_clean = re.sub(r'<h2.{0,}', '<p>**<', regex_text_clean)
    regex_text_clean = re.sub(r'<h3.{0,}', '<p>***<', regex_text_clean)
    regex_text_clean = re.sub(r'<h4.{0,}', '<p>****<', regex_text_clean)
    regex_text_clean = re.sub(r'<h5.{0,}', '<p>*****<', regex_text_clean)
    regex_text_clean = re.sub(r'<h6.{0,}', '<p>******<', regex_text_clean)

    # heading end
    regex_text_clean = re.sub(r'</h1>.{0,}', '>*<p>', regex_text_clean)
    regex_text_clean = re.sub(r'</h2>.{0,}', '>**<p>', regex_text_clean)
    regex_text_clean = re.sub(r'</h3>.{0,}', '>***<p>', regex_text_clean)
    regex_text_clean = re.sub(r'</h4>.{0,}', '>****<p>', regex_text_clean)
    regex_text_clean = re.sub(r'</h5>.{0,}', '>*****<p>', regex_text_clean)
    regex_text_clean = re.sub(r'</h6>.{0,}', '>******<p>', regex_text_clean)

    soup = BeautifulSoup(regex_text_clean, 'html.parser')

    article_text = ""

    paragraph_list = []

    a = soup.find_all('p')

    for i in a:
        article_text += i.text

    string = unique_lines_as_string(article_text)

    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', string)
    article_text = re.sub(r'[*]+[\s]+[*]+ ', '', article_text)
    article_text = re.sub(r' +', ' ', article_text)
    article_text = re.sub(r'><', '', article_text)
    article_text = re.sub(r'\n+ ', '\n', article_text)
    article_text = re.sub(r'\n+', '\n', article_text)

    article_text = re.sub(r'[<>*]+', '', article_text)
    article_summary_str = re.sub(r'[ \n]{3,}', '\n\n', article_text)

    # TODO: Could be cleaned up. Duplicates just not added.
    if extract_by_numbers_only:
        key_points = []

        for i in article_summary_str.splitlines():
            if has_numbers(i[0:2]):
                key_points.append(i)

        if punc_in_first_three_chars:
            key_points = [s for s in key_points if any(xs in s[0:4] for xs in [',', '.', '#'])]

        # print(key_points)
        unique_key_points = remove_dupl_pres_order(key_points)
        article_summary_str = '\n'.join(unique_key_points)

        filename += '_EBN'

    overwrite_file(f'{filename}.txt', url + '\n\n' + article_summary_str)

    return article_summary_str

def extract_html_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    page = requests.get(url, headers=headers)
    parsed_article = BeautifulSoup(page.text, 'lxml')
    return parsed_article

def extract_headers_by_url(url, extract_by_numbers_only=False, filename='data_grab'):
    # # TODO Address and understand headers requirements of requests.
    parsed_article = extract_html_from_url(url)
    body = parsed_article.find('body')

    headers_set = set()

    for i in parsed_article.find_all('h3'):
        if i.text not in headers_set:
            headers_set.add(i.text)

    for i in headers_set:
        print(i,'\n-----------------------')

    # return

def run_google_search(search, top_lvl_domain='.com'):

    if top_lvl_domain[0] != '.':
        top_lvl_domain = '.' + top_lvl_domain

    # print(top_lvl_domain)

    word_list_exc_punc = re.split(r'\W+', search)
    search_string = '+'.join(word_list_exc_punc)

    url = rf'https://www.google{top_lvl_domain}/search?q={search_string}'

    soup = extract_html_from_url(url)

    search_results_list = (soup.find_all("div", {"class": "g"}))

    search_results_url_list = []

    for result in search_results_list:
        search_results_url_list.append(result.find('a')['href'])

    return search_results_url_list


def extract_content_by_google_search(google_search, number_of_results=100, extract_by_numbers_only=False):
    all_urls = list(set(run_google_search(google_search)))
    results = all_urls[0:min(len(all_urls), number_of_results)]

    index = 0
    for url in results:
        extract_content_by_url(url, extract_by_numbers_only, google_search + '_' + str(index))
        index += 1

    print('Completed')


if __name__ == '__main__':
    google_search = 'top 10 ways to make money'
    # extract_content_by_google_search(google_search, 5, True)

    # url = r'https://www.inc.com/rhett-power/10-ways-make-earn-money-fast.html'
    # url = r'https://www.savethestudent.org/make-money/10-quick-cash-injections.html'
    url = 'https://www.oberlo.co.uk/blog/how-to-make-money-online'

    # extract_headers_by_url(url)
    a = extract_content_by_url(url=url, extract_by_numbers_only=True)
