import requests
from lxml import html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_TITLE = '//div[@class = "mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class = "lead"]/p/text()'
XPATH_BODY = '//div[@class = "html-content"]/p/text() | //div[@class = "html-content"]/p/*/text()'


def parse_notice(link, today):
    """
    Extract the title, summary and body from the notice link
    """
    try:
        response = requests.get(link)
        if response.status_code == 200:
            # extract html and transform to string
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                # extract title, summary and body
                title = parsed.xpath(XPATH_TITLE)[0] 
                title = title.strip()
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY) 
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                # create the file and add data 
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for paragraph in body:
                    f.write(paragraph)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    """
    Extract the links to notices, and call parse notice() to extract data from the links
    """
    try:
        response = requests.get(HOME_URL)

        if response.status_code == 200:
            # Extract links and get date
            home = response.content.decode('utf-8') 
            parsed = html.fromstring(home) 
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%y-%m-%d')

            if not os.path.isdir(today):
                # Create directory
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()