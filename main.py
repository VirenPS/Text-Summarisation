import heapq
import re
import urllib.request

import nltk
from bs4 import BeautifulSoup

from my_utils import write_to_file

url = 'https://webflow.com/blog/website-ideas'
# url = 'https://www.investopedia.com/articles/pf/08/make-money-in-business.asp'

scraped_data = urllib.request.urlopen(url)

article = scraped_data.read()

parsed_article = BeautifulSoup(article,'lxml')


# html_components = ['div', 'h1', 'h2', 'h3', 'h4']

# Find number of each element type and build a dictionary


body = parsed_article.find('body')
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

body_string = body.prettify()

regex_text_clean = re.sub(r'<h1.{0,}', '<p>*', body_string)
regex_text_clean = re.sub(r'<h2.{0,}', '<p>**', regex_text_clean)
regex_text_clean = re.sub(r'<h3.{0,}', '<p>***', regex_text_clean)
regex_text_clean = re.sub(r'<h4.{0,}', '<p>****', regex_text_clean)
regex_text_clean = re.sub(r'<h5.{0,}', '<p>*****', regex_text_clean)
regex_text_clean = re.sub(r'<h6.{0,}', '<p>******', regex_text_clean)

regex_text_clean = re.sub(r'</h1>.{0,}', '*<p>', regex_text_clean)
regex_text_clean = re.sub(r'</h2>.{0,}', '**<p>', regex_text_clean)
regex_text_clean = re.sub(r'</h3>.{0,}', '***<p>', regex_text_clean)
regex_text_clean = re.sub(r'</h4>.{0,}', '****<p>', regex_text_clean)
regex_text_clean = re.sub(r'</h5>.{0,}', '*****<p>', regex_text_clean)
regex_text_clean = re.sub(r'</h6>.{0,}', '******<p>', regex_text_clean)

soup = BeautifulSoup(regex_text_clean, 'html.parser')

article_text = ""

paragraph_list = []

a = soup.find_all('p')

for i in a:
    article_text += i.text

seen = set()
answer = []

for line in article_text.splitlines():
    if (line not in seen) or '*' in line:
        seen.add(line)
        answer.append(line)

string = '\n'.join(answer)

# Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', string)
article_text = re.sub(r'[*]+[\s]+[*]+', '', article_text)
article_text = re.sub(r' +', ' ', article_text)
article_text = re.sub(r'\n+ ', '\n', article_text)
article_text = re.sub(r'\n+', '\n', article_text)

print(article_text)

write_to_file('temp.txt', article_text)
