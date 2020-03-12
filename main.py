import requests, os, re
from config_reader import *
import json
import mat

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
    def __init__(self, tag=None, author_id=None, mode='all'):
        self.tag = tag
        self.author_id = author_id
        self.mode = mode

    def get_illusts_by_author(self, id):
        # &p=1
        url = 'https://www.pixiv.net/ajax/user/{id}/profile/all'.format(id=str(id))
        img_ids = []
        proxies = get_proxies()
        headers = get_headers()
        res = requests.get(url, proxies=proxies, headers=headers)
        data = json.loads(res.content)
        try:
            illusts = data['body']['illusts']
            for illust in illusts.keys():
                img_ids.append(illust)
        except KeyError:
            pass
        return img_ids

    def get_illusts_by_id(self, img_ids):
        img_urls = []
        for img_id in img_ids:
            url = 'http://pixiv.net/ajax/illust/{id}/pages'.format(id=str(img_id))
            proxies = get_proxies()
            headers = get_headers()
            res = requests.get(url, proxies=proxies, headers=headers)
            data = json.loads(res.content)

            count = 0
            for img in data['body']:
                count += 1
                if count > 10:
                    break
                img_url = img['urls']['original'].split('img')[-1]
                img_url = 'https://tc-pximg01.techorus-cdn.com/img-original/img' + img_url
                print(img_url)
                img_urls.append(img_url)
        return img_urls

    def save_img(self, img_url):
        proxies = get_proxies()
        img_dir = get_img_dir()

        res = requests.get(img_url, proxies=proxies)
        print(res)
        name = img_url.split('/')[-1]

        path = os.path.join(img_dir, name)
        with open(path, 'wb') as fw:
            print(path)
            fw.write(res.content)
            print('picture %s is ok' % name)
            fw.close()

    def get_tag_rank(self, tag, mode):
        page = 1
        count = 0   #画数
        authors = {}    #作者id对应其作品数目
        while True:
            url = 'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}' \
              '&order=date_d&mode={mode}&p={page}&s_mode=s_tag&type=all'.format(page=str(page), tag=tag, mode=mode)
            print('page={p}'.format(p=str(page)))


            res = requests.get(url, proxies=get_proxies(), headers=get_headers())
            with open('test.json', 'wb') as fw:
                fw.write(res.content)
                a = json.loads(res.content, encoding='utf-8')
                a = a['body']['illustManga']['data']

                # 如果得到空集停止循环
                if not a:
                    break

                for b in a:
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
            page += 1
        print(count)
        d = {}
        for x in [x for x in authors.keys() if authors[x] > 5]:
            d[x] = authors[x]
        mat.plt_barh(d, tag)




if __name__ == '__main__':
    px = Pixiv()
    px.get_tag_rank(tag='東方Project10000users入り', mode='safe')