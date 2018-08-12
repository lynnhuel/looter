import looter as lt
from concurrent import futures

domain = 'https://xkcd.com'

def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.css('#comic img::attr(src)').extract()
    lt.save_imgs(imgs)


if __name__ == '__main__':
    tasklist = [f'{domain}/{i}' for i in range(1, 1960)]
    with futures.ThreadPoolExecutor(30) as executor:
        executor.map(crawl, tasklist)