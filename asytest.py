from asyncio import *
import random, time
import asyncio, aiofiles, aiohttp
from aiohttp_requests import requests
from config_reader import *
import json


async def test1(string):
    print('test1')
    await sleep(1.8+random.random())
    print(string)


async def test2(string):
    print('test2')
    await sleep(4)
    print(string)


async def get_res(url):
    res = await requests.get(url, proxy=get_proxies(), headers=get_headers())
    return res

proxy = 'http://127.0.0.1:1080'


async def get_tag_rank(tag, mode='all'):
    begin_time = time.time()
    page = 1
    count = 0  # 画数
    authors = {}  # 作者id对应其作品数目

    # 申请第一页得到作品数，每页有60个id
    first_url = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date_d&mode={mode}&p=1&s_mode=s_tag&type=all'
    print(first_url)
    first_res = await requests.get(first_url, proxy=proxy, headers=get_headers())
    first_content = await first_res.json()

    # for a in first_content['body']['illustManga']['data']:
    #     print(a)
    max_page = int(int(first_content['body']['illustManga']['total']) / 60) + 2
    print('all:', first_content['body']['illustManga']['total'])
    print('最大页数', max_page)



    all_res = []
    # 建立n个任务,一个任务对应1个page
    for n in range(1, max_page):
        print(f'page={page}')
        url = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}' \
              f'&order=date_d&mode={mode}&p={page}&s_mode=s_tag&type=all'
        res = await requests.get(url, proxy=proxy, headers=get_headers())
        all_res.append(res)
        page += 1

        info_json = await res.json()
        illust_infos = info_json['body']['illustManga']['data']

        for b in illust_infos:
            try:
                print(b['userName'])
            except KeyError:
                print('no username')
                continue
            try:
                authors[b['userName']] += 1
            except KeyError:
                authors[b['userName']] = 1
            try:
                print(b['illustTitle'])
            except KeyError:
                print('no title')
                continue
            count += 1
    print('use times:', time.time() - begin_time)


if __name__ == '__main__':
    run(get_tag_rank('東方Project10000users入り', mode='r18'))