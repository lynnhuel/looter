import pymongo
from requestium import Session
from pprint import pprint

domain = 'https://hitomi.la'
client = pymongo.MongoClient()
db = client.hitomi
col = client.gamecg

def crawl(url):
    s.driver.get(url)
    gallery_content = s.driver.find_elements_by_css_selector('.gallery-content > div')
    for gallery in gallery_content:
        data = dict()
        data['title'] = gallery.find_element_by_css_selector('h1 a').text
        data['link'] = gallery.find_element_by_css_selector('a').get_attribute('href')
        data['artist'] = ', '.join([a.text for a in gallery.find_elements_by_css_selector('.artist-list ul li')])
        desc = gallery.find_element_by_css_selector('table.dj-desc')
        data['series'] = desc.find_element_by_css_selector('tr:first-child td:nth-child(2)').text
        data['type'] = desc.find_element_by_css_selector('tr:nth-child(2) td:nth-child(2) a').text
        data['language'] = desc.find_element_by_css_selector('tr:nth-child(3) td:nth-child(2) a').text
        data['tags'] = ', '.join([li.text for li in desc.find_elements_by_css_selector('tr:nth-child(4) td:nth-child(2) ul li')])
        data['date'] = gallery.find_element_by_css_selector('p.date').text
        pprint(data)
        col.insert_one(data)

if __name__ == '__main__':
    s = Session(webdriver_path='D:\\Program Files (x86)\\chromedriver\\chromedriver.exe', browser='chrome', default_timeout=30, webdriver_options={'arguments': ['headless']})
    tasklist = [f'{domain}/type/gamecg-all-{n}.html' for n in range(1, 100)]
    result = [crawl(task) for task in tasklist]