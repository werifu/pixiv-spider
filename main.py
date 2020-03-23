import os
from config_reader import *
import asyncio, aiofiles, aiohttp
from aiohttp_requests import requests
import json, mat, time



class Author():
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name


    @property
    def get_name(self):
        return self.name

    @property
    def get_id(self):
        return self.id


class Pixiv():

    #mode默认为'all'，可以选择'safe' || 'r18'
    def __init__(self, tag=None, author_id=None, mode='all', proxy=None):
        self.tag = tag
        self.author_id = author_id
        self.mode = mode
        self.proxy = proxy


    async def get_illusts_by_author(self, id):
        # &p=1
        url = 'https://www.pixiv.net/ajax/user/{id}/profile/all'.format(id=str(id))
        img_ids = []
        headers = get_headers()
        res = await requests.get(url, proxy=self.proxy, headers=headers)
        data = await res.json()
        try:
            illusts = data['body']['illusts']
            for illust in illusts.keys():
                img_ids.append(illust)
        except KeyError:
            pass
        return img_ids

    async def get_illusts_by_id(self, img_ids):
        img_urls = []
        for img_id in img_ids:
            url = 'http://pixiv.net/ajax/illust/{id}/pages'.format(id=str(img_id))
            headers = get_headers()

            res = await requests.get(url, proxy=self.proxy, headers=headers)
            data = await res.json()

            count = 0
            for img in data['body']:
                count += 1
                if count > 10:
                    break
                img_url = img['urls']['original'].split('img')[-1]
                img_url = 'https://tc-pximg01.techorus-cdn.com/img-original/img' + img_url
                # print(img_url)
                # start = time.time()

                img_urls.append(img_url)
                # print('use time:', time.time() - start)
        return img_urls

    async def save_img(self, img_url):
        img_dir = get_img_dir()

        res = await requests.get(img_url, proxy=self.proxy)
        print(res)
        name = img_url.split('/')[-1]

        path = os.path.join(img_dir, 'nakatani\\', name)
        async with aiofiles.open(path, 'wb') as fw:
            print(path)
            await fw.write(await res.read())
            print('picture %s is ok' % name)
            fw.close()

    async def get_tag_rank(self, tag, mode='all'):
        begin_time = time.time()
        page = 1
        count = 0  # 画数
        authors = {}  # 作者id对应其作品数目

        # 申请第一页得到作品数，每页有60个id
        first_url = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date_d&mode={mode}&p=1&s_mode=s_tag&type=all'
        print("first:", first_url)
        first_res = await requests.get(first_url, proxy=self.proxy, headers=get_headers())
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
            print(url)
            res = await requests.get(url, proxy=self.proxy, headers=get_headers())
            all_res.append(res)
            page += 1

            info_json = await res.json()
            illust_infos = info_json['body']['illustManga']['data']

            for b in illust_infos:
                try:
                    b['userName']
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

        d = {}
        max_num = 0
        for x in [x for x in authors.keys() if authors[x] > 60]:
            if authors[x] > max_num:
                max_num = authors[x]
            d[x] = authors[x]
        mat.plt_barh(d, tag, max_num=200)


async def main():
    px = Pixiv()
    px.proxy = 'http://127.0.0.1:1080'
    start = time.time()
    ids = await px.get_illusts_by_author(123216)
    urls = await px.get_illusts_by_id(ids)
    i = 0
    while i < len(urls):
        tasks = []
        for x in range(15):
            try:
                tasks.append(px.save_img(urls[i]))
                i += 1
            except IndexError:    #到尽头了
                break
        await asyncio.gather(*tasks)

    end = time.time()
    print('use time:'+str(end-start))


if __name__ == '__main__':
    asyncio.run(main())