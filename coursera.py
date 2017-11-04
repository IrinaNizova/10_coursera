import requests
import argparse
from lxml import html
from bs4 import BeautifulSoup
from openpyxl import Workbook
import logging

logging.basicConfig(level=logging.INFO)


def get_courses_list(count_courses=20):
    response = requests.get('https://www.coursera.org/sitemap~www~courses.xml')
    courses_content = html.fromstring(response.content)
    courses_elements = courses_content.xpath('//url/loc')[:count_courses]
    return [courses_element.text for courses_element in courses_elements]


def get_course_info(course_url):

    requests_course_data = get_course_page_content(course_url)
    course_attribs = parse_course_content(requests_course_data)
    print_course_attrs(course_url, *course_attribs)

    return course_attribs


def get_course_page_content(course_url):
    return requests.get(course_url).content


def parse_course_content(requests_course_content):
    soup = BeautifulSoup(requests_course_content, 'html.parser')
    course_caption = soup.find('h1').string
    course_rating = \
        soup.find("div", {"class": "ratings-text bt3-visible-xs"})
    course_rating = \
        course_rating.string.strip(' stars') if course_rating else ''
    course_lang = \
        list(soup.find("div", {"class": "language-info"}).div.children)[1]
    course_start_date = soup.find("div", {"class": "startdate"}).span.string
    course_week_count = str(len(soup.find_all("div", {"class": "week-body"})))
    course_attribs = (course_caption, course_lang, course_rating,
        course_week_count, course_start_date)
    return course_attribs


def print_course_attrs(course_url, *course_attribs):

    course_caption, course_lang, course_rating, course_week_count, course_start_date = course_attribs
    logging.info(course_url)
    logging.info('Caption: {}'.format(course_caption))
    logging.info('Language: {}'.format(course_lang))
    logging.info('Stars: {}'.format(course_rating))
    logging.info('Duration: {}'.format(course_week_count))
    logging.info('Start date: {}'.format(course_start_date))


def output_courses_info_to_xlsx(courses_info, filepath_to_save):
    wb = Workbook()
    ws = wb.active
    for row in courses_info:
        ws.append(row)
    wb.save(filepath_to_save if filepath_to_save else 'courses_info.xlsx')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', '--count', type=int, required=False)
    parser.add_argument('-f', '--filepath', type=str, required=False)
    script_args = parser.parse_args()

    if script_args.count:
        courses_urls = get_courses_list(script_args.count)
    else:
        courses_urls = get_courses_list()
    courses_properties = [('Caption', 'Language', 'Stars', 'Duration', 'Start date')]
    for course_url in courses_urls:
        courses_properties.append(get_course_info(course_url))

    output_courses_info_to_xlsx(courses_properties, script_args.filepath)
