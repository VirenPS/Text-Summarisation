import heapq
import re

import nltk
# from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup

from utils import (has_numbers, unique_lines_as_list, unique_lines_as_string,
                   write_to_file)


def extract_html_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    page = requests.get(url, headers=headers)
    parsed_article = BeautifulSoup(page.text, 'lxml')
    return parsed_article

def extract_key_points(url, extract_by_numbers_only=False, filename='data_grab'):
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

    if extract_by_numbers_only:
        key_points = []
        article_summary_str = re.findall(r'[*]+<[\s\S]([\s\S]*?)>[*]+[\s\S]', article_text)
        for i in article_summary_str:
            try:
                if has_numbers(i[0:3]):
                    key_points.append(i)
            except Exception as e:
                print(e)
                pass
        article_summary_str = ''.join(key_points)
    else:
        article_text = re.sub(r'[<>*]+', '', article_text)
        article_text = re.sub(r'[ \n]{3,}', '\n\n', article_text)
        article_summary_str = ''.join(article_text)

    write_to_file(f'{filename}.txt', article_summary_str)

    return article_summary_str

    # article_summary_list = unique_lines_as_list(article_summary)

    # print(article_summary_list)

    # print(header)


def run_google_search(search, number_of_results = 5, top_lvl_domain='.co.uk'):

    if top_lvl_domain[0] != '.':
        top_lvl_domain = '.' + top_lvl_domain

    # print(top_lvl_domain)

    word_list_exc_punc = re.split(r'\W+', search)
    search_string = '+'.join(word_list_exc_punc)

    url = rf'https://www.google{top_lvl_domain}/search?q={search_string}'

    soup = extract_html_from_url(url)

    search_results_list = (soup.find_all("div", {"class": "g"}))[0:number_of_results]

    search_results_url_list = []

    for result in search_results_list:
        search_results_url_list.append(result.find('a')['href'])

    return search_results_url_list


def extract_content_by_google_search(google_search, extract_by_numbers_only):
    results = run_google_search(google_search)

    index = 0
    for url in results:
        extract_key_points(url, True, google_search + '_' + str(index))
        index += 1

    print('Completed')


if __name__ == '__main__':
    # url = r'https://www.investopedia.com/articles/pf/08/make-money-in-business.asp'
    # url = r'https://webflow.com/blog/website-ideas'
    # url = r'https://www.google.com/search?q=ipl+score&oq=ipl&aqs=chrome.0.69i59j46i131i433i512j0i131i433i512j46i199i291i433i512j69i60l4.616j0j7&sourceid=chrome&ie=UTF-8#sie=m;/g/11nxsks048;5;/m/03b_lm1;dt;fp;1;;'
    # url = r'https://www.google.com/search?q=ipl+score&oq=ipl'
    # url = 'https://docs.python.org/3/howto/urllib2.html'
    # url = r'https://www.entrepreneur.com/article/293954'

    # Fix header issue and investigate
    # url = r'https://www.lifehack.org/articles/lifestyle/how-to-be-successful-in-life.html'

    # Small issue highlighted by blog.hubspot.com below - TODO 1st heading/ Main title clash causing 1st heading dropoff
    # url = r'https://blog.hubspot.com/marketing/best-website-designs-list'
    # url = r'https://www.upwork.com/ab/find-work/domestic'

    # url = r'https://freshysites.com/web-design-development/most-popular-websites/'
    # content = extract_key_points(url, True, 2)

    extract_content_by_google_search('Top 10 most useful skills')


