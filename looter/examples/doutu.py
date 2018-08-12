import looter as lt
from concurrent import futures

domain = 'https://www.doutula.com'

def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.css('img.lazy::attr(data-original)').extract()
    lt.save_imgs(imgs)


if __name__ == '__main__':
    tasklist = [f'{domain}/article/list/?page={i}' for i in range(1, 551)]
    with futures.ThreadPoolExecutor(50) as executor:
        executor.map(crawl, tasklist)