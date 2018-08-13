.. looter documentation master file, created by
   sphinx-quickstart on Tue Jul 31 11:28:11 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Looter: Web-Scraping for Humans!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

|build| |grade|

.. |build| image:: https://api.travis-ci.org/alphardex/looter.svg
    :target: https://api.travis-ci.org/alphardex/looter

.. |grade| image:: https://api.codacy.com/project/badge/Grade/78dbe75cccef4c5887ea236e9afcb89e    
    :target: https://www.codacy.com/project/alphardex/looter/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alphardex/looter&amp;utm_campaign=Badge_Grade_Dashboard

A super-lightweight crawler tool.

-  automatically generate spider with template
-  blazing fast speed with concurrent.futures or asyncio
-  provides shell to debug your spider
-  easy web content extracting with parsel (just the same as Scrapy)
-  fake-useragent included (disguise as a web browser)
-  built in many useful functions
-  provides many examples for you to start

Installation
============

.. code-block:: shell

    $ pip install looter

Only **Python 3.6** is supported.

Quick start
============

Here's a very simple image crawler: First, open it with shell

.. code:: bash

    $ looter shell konachan.com/post

Then, you can crawl all the images of the page in just 2-line code

.. code:: python

    >>> imgs = tree.css('a.directlink::attr(href)').extract()
    >>> save_imgs(imgs)

Or if you want, just 1-line is OK :d

.. code:: python

    >>> save_imgs(links(res, search='jpg'))

Workflow
========

If you want to quickly write a spider, you can use looter to
automaticaly generate one :)

.. code:: python

    $ looter genspider <name> <tmpl> [--async]

In this code, **tmpl** is template, inculdes **data and image**.

**async** is an option which represents generating a spider using
**asyncio** instead of threadpool.

In the generated template, you can custom the **domain**, and the
**tasklist**.

What is **tasklist**? Actually it is **the pages you want to crawl** and
that's it.

You can simply **use list comprehension to make your own tasklist**,
using konachan.com as example:

.. code:: python

    domain = 'https://konachan.com'
    tasklist = [f'{domain}/post?page={i}' for i in range(1, 9777)]

And then you should custom your **crawl** function, which is the core of
your spider.

.. code:: python

    def crawl(url):
        tree = lt.fetch(url)
        items = tree.css('ul li')
        for item in items:
            data = dict()
            # data[...] = item.css(...)
            pprint(data)

In most cases, the contents you want to crawl is a list (ul or ol tag in
HTML), you can select them as items.

Then, just use a for loop to iterate them, and select the things you
want, storing them to a dict.

**Notice: looter use parsel to parse the HTML, just the same as Scrapy.**

But before you finish this spider, you'd better debug your codes using shell provided by looter.

.. code:: python

    >>> items = tree.css('ul li')
    >>> item = items[0]
    >>> item.css(anything you want to crawl)
    # Pay attention to the outputs!

After debugging, your spider is done. Very simple, isn't it :)

There are \ `many example spiders <https://github.com/alphardex/looter/tree/master/looter/examples>`__ written by author.

Functions
=========

Looter also provides many useful functions for you.

view
----

Before crawling a page, you'd better check whether it's rendered
properly

.. code:: python

    >>> view(url)

save\_imgs
----------

Once you get a list of image links, use it to grab them all! [has async
version]

.. code:: python

    >>> img_urls = [...]
    >>> save_imgs(img_urls)

alexa\_rank
-----------

Get the reach and popularity of a site in alexa. It will return a tuple:
(url, reach\_rank, popularity\_rank)

.. code:: python

    >>> alexa_rank(url)

links
-----

Get all the links of the page.

.. code:: python

    >>> links(res)                  # get all the links
    >>> links(res, absolute=True)   # get all the absolute links
    >>> links(res, search='text')   # search the links you want

Also, you can use regex pattern

.. code:: python

    >>> re_links(res, r'regex_pattern')

save\_as\_json
--------------

Save what you crawled as a json file, supports sorting.

.. code:: python

    >>> total = [...]
    >>> save_as_json(total, name='text', sort_by='key')

parse\_robots
-------------

Parse the robots.txt of the site and retrieve its urls.

.. code:: python

    >>> parse_robots(url)

login
-----

Login the site using POST request, data required.

.. code:: python

    >>> params = {'df': 'mail126_letter', 'from': 'web', 'funcid': 'loginone', 'iframe': '1', 'language': '-1', 'passtype': '1', 'product': 'mail126',
     'verifycookie': '-1', 'net': 'failed', 'style': '-1', 'race': '-2_-2_-2_db', 'uid': 'webscraping123@126.com', 'hid': '10010102'}
    >>> postdata = {'username': ..., 'savelogin': '1', 'url2': 'http://mail.126.com/errorpage/error126.htm', 'password': ...}
    >>> url = "https://mail.126.com/entry/cgi/ntesdoor?"
    >>> res, ses = login(url, postdata, params=params)
    >>> index_url = re.findall(r'href = "(.*?)"', res.text)[0]
    >>> index = ses.get(index_url)

Summary
=======

1. By sniffing, confirm whether the website has its own api. If it does, take it! If not, go to the next step.
2. Confirm whether the website is static or dynamic (with or without JS loading, whether requires login, etc), the methods are: observation, sniffing and looter 's view function
3. If the website is static, use 'looker genspider' to generate a spider template, and then use 'looter shell' to debug and make your spider.
4. If the website is dynamic, sniff first, and try to get all the api links generated by ajax; if there is no api, go to the next step.
5. Some websites do not directly expose their ajax api link. In this case, you need to construct the api link according to the rules.
6. If it doesn't work, then you have to use \ `requestium <https://github.com/tryolabs/requestium>`__\  to render the JS and crawl the page.
7. As for the problem of \ `login <https://github.com/xchaoinfo/fuck-login>`__\, \ `IP Proxy <https://github.com/imWildCat/scylla>`__\, Captcha, distributed crawler and so on, plz work them out by yourself.
8. If your crawler project is required to use Scrapy, then you can also copy the parsing code of the looter to Scrapy painlessly (both of them use parsel after all)

Once you've mastered all the steps above, you can almost crawl everything you want!
