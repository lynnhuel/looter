import looter as lt
from concurrent import futures

domain = 'https://xkcd.com'

def crawl(url):
    tree = lt.fetch(url)
    imgs = tree.css('#comic img::attr(src)').extract()
    print(imgs)
    lt.async_save_imgs(imgs)


if __name__ == '__main__':
    tasklist = [f'{domain}/{i}' for i in range(1, 1960)]
    result = [crawl(task) for task in tasklist]