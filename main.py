import heapq
import re
import urllib.request

import nltk
from bs4 import BeautifulSoup

from my_utils import (has_numbers, unique_lines_as_list,
                      unique_lines_as_string, write_to_file)


def extract_key_points(url, extract_by_numbers=False):
    # # TODO Address and understand headers requirements of requests.
    # hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #     'Accept-Encoding': 'none',
    #     'Accept-Language': 'en-US,en;q=0.8',
    #     'Connection': 'keep-alive'}



    scraped_data = urllib.request.urlopen(url)

    article = scraped_data.read()

    parsed_article = BeautifulSoup(article,'lxml')


    # html_components = ['div', 'h1', 'h2', 'h3', 'h4']

    # Find number of each element type and build a dictionary


    # write_to_file('html_body_test.txt',content=paragraphs.prettify())
    # print(paragraphs)

    # # create a sorted unique list of all html tags
    # html_tags = []
    # for tag in body.findAll(True):
    #     html_tags.append(tag.name)

    # unique_html_tags = sorted(list(set(html_tags)))
    # html_header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    # header_tags_contained = sorted(list(set(unique_html_tags).intersection(html_header_tags)))

    # # print(header_tags_contained)


    # temp = body.find_all('h2')
    # # print(type(temp))

    # container = []

    # for i in header_tags_contained:
    #     temp_list = []
    #     for tag in body.find_all(i):
    #         temp_list.append(tag.text)

    #     container.append(temp_list)

    # print(container)


    # body_string = body.prettify()

    # print(body_string)

    # convert <h*> tags into <p>**
    # h1 into <p>*
    # h2 into <p>**
    # h3 into <p>***
    # h4 into <p>****

    body = parsed_article.find('body')

    body_string = body.prettify()

    # replace heading tags with fancy paragraphs, so we can later identify heading level in text extracted / order of heading to paragraph.
    regex_text_clean = re.sub(r'<h1.{0,}', '<p>*<', body_string)
    regex_text_clean = re.sub(r'<h2.{0,}', '<p>**<', regex_text_clean)
    regex_text_clean = re.sub(r'<h3.{0,}', '<p>***<', regex_text_clean)
    regex_text_clean = re.sub(r'<h4.{0,}', '<p>****<', regex_text_clean)
    regex_text_clean = re.sub(r'<h5.{0,}', '<p>*****<', regex_text_clean)
    regex_text_clean = re.sub(r'<h6.{0,}', '<p>******<', regex_text_clean)

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

    # seen = set()
    # answer = []

    # for line in article_text.splitlines():
    #     if (line not in seen) or '*' in line:
    #         seen.add(line)
    #         answer.append(line)

    string = unique_lines_as_string(article_text)

    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', string)
    article_text = re.sub(r'[*]+[\s]+[*]+', '', article_text)
    article_text = re.sub(r' +', ' ', article_text)
    article_text = re.sub(r'><', '', article_text)
    article_text = re.sub(r'\n+ ', '\n', article_text)
    article_text = re.sub(r'\n+', '\n', article_text)

    # Extract Heading Titles
    # header = re.findall(r'[*]+<\n([\s\S]*?)>[*]+\n.', article_text)
    article_summary = re.findall(r'[*]+<[\s\S]([\s\S]*?)>[*]+[\s\S]', article_text)

    if extract_by_numbers:
        key_points = []
        for i in article_summary:
            try:
                if has_numbers(i[0:3]):
                    key_points.append(i)
            except:
                pass
        return key_points

    write_to_file('temp2.txt', key_points)
    return article_summary

    # article_summary_list = unique_lines_as_list(article_summary)

    # print(article_summary_list)

    # print(header)


if __name__ == '__main__':
    # url = r'https://www.investopedia.com/articles/pf/08/make-money-in-business.asp'
    # url = r'https://webflow.com/blog/website-ideas'

    # Fix header issue and investigate
    # url = r'https://www.entrepreneur.com/article/293954'
    # url = r'https://www.lifehack.org/articles/lifestyle/how-to-be-successful-in-life.html'

    # url = r'https://freshysites.com/web-design-development/most-popular-websites/'

    # Small issue highlighted by blog.hubspot.com below - TODO 1st heading/ Main title clash causing 1st heading dropoff
    url = r'https://blog.hubspot.com/marketing/best-website-designs-list'

    key_points_str = ''.join(extract_key_points(url, True))
    write_to_file('temp.txt', key_points_str)

    print(key_points_str)
