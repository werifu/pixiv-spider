import requests, os, re
from config_reader import *
import json
import time


def get_illusts_by_auther(id):
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


def get_illusts_by_id(img_ids):
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


def save_img(img_url):
    proxies = get_proxies()
    img_dir = get_img_dir()

    res = requests.get(img_url, proxies=proxies)
    print(res)
    name = img_url.split('/')[-1]

    path = os.path.join(img_dir, 'UUZan\\', name)
    with open(path, 'wb') as fw:
        print(path)
        fw.write(res.content)
        print('picture %s is ok' % name)
        fw.close()


def main():
    img_ids = get_illusts_by_auther(2179695)
    print(img_ids)
    img_urls = get_illusts_by_id(img_ids)
    # print(img_urls)
    # for img_url in img_urls:
    #     save_img(img_url)


if __name__ == '__main__':
    count = 0
    t = time.time()
    authers = {}
    for p in range(1, 20):
        url = 'https://www.pixiv.net/ajax/search/artworks/東方Project100000users入り?word=東方Project100000users入り' \
          '&order=date_d&mode=r18&p={page}&s_mode=s_tag&type=all'.format(page=p)
        proxies = get_proxies()
        res = requests.get(url, proxies=proxies, headers=get_headers())
        with open('test.json', 'wb') as fw:
            fw.write(res.content)
            a = json.loads(res.content, encoding='utf-8')
            a = a['body']['illustManga']['data']
            if a is []:
                break
            for b in a:
                try:
                    b['userName']
                except KeyError:
                    continue
                try:
                    authers[b['userName']] += 1
                except KeyError:
                    authers[b['userName']] = 1
                try:
                    print(b['illustTitle'])
                except KeyError:
                    continue
                count += 1
    print(time.time()-t)
    print(count)
    print([x for x in authers.keys() if authers[x] > 5])