import pymongo
import looter as lt
from pprint import pprint
from concurrent import futures

domain = 'https://www.javbus.pw'
client = pymongo.MongoClient()
db = client.jav
col = db.torrents

def crawl(url):
    tree = lt.fetch(url)
    items = tree.css('#waterfall .item')
    for item in items:
        data = dict()
        data['name'] = item.css('img::attr(title)').extract_first()
        data['cover'] = item.css('img::attr(src)').extract_first()
        data['link'] = item.css('.movie-box::attr(href)').extract_first()
        data['bango'] = item.css('date::text').extract_first()
        data['date'] = item.css('date::text').extract()[1]
        pprint(data)
        col.insert_one(data)


if __name__ == '__main__':
    tasklist = [f'{domain}/page/{i}' for i in range(1, 90)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)
