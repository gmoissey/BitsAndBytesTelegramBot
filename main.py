from datetime import timedelta, datetime
from dateutil import parser
from pprint import pprint
from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import feedparser
import config

BOT_TOKEN = config.BOT_TOKEN
CHANNEL_ID = config.CHANNEL_ID
FEED_URL = config.FEED_URL

def send_message(content):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/{content}')


def main():
    rss_feed = feedparser.parse(FEED_URL)

    for entry in rss_feed.entries:

        parsed_date = parser.parse(entry.published)
        parsed_date = (parsed_date - timedelta(hours=0)).replace(tzinfo=None) # remove timezone offset
        now_date = datetime.utcnow()
        
        
        published_30_minutes_ago = now_date - parsed_date < timedelta(minutes=(60 * 24))


        if (published_30_minutes_ago):
            
            photoURL = entry.link

            try:
                html = urlopen(entry.link)
                bs = BeautifulSoup(html, 'html.parser')
                images = bs.find_all('img', {'src':re.compile('.jpg')})
                photoURL = images[0]['src']
            except:
                pass

            try:
                html = urlopen(entry.link)
                bs = BeautifulSoup(html, 'html.parser')
                images = bs.find_all('img', {'src':re.compile('.png')})
                photoURL = images[0]['src']
            except:
                pass
    

            title = entry.title
            summary = entry.summary
            link = entry.link

            if(photoURL == entry.link):
                content = ("<b>%s\n</b>%s\n<a href=\"%s\">Continue Reading...</a><a href=\"%s\">.</a>" % (title, summary, link, photoURL))
                message = f'sendMessage?chat_id={CHANNEL_ID}&text={content}&parse_mode=HTML'
                send_message(message)
            else:
                content = ("<b>%s\n</b>%s\n<a href=\"%s\">Continue Reading...</a>" % (title, summary, link))
                message = f'sendPhoto?chat_id={CHANNEL_ID}&photo={photoURL}&caption={content}&parse_mode=HTML'
                send_message(message)
            



if __name__ == "__main__":
    while(True):
        main()
        sleep(60 * 60 * 24)
