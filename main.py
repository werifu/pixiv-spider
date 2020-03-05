import requests, os, re
from config_reader import *
import json


def get_illusts_by_auther(id):
    # &p=1
    url = 'https://www.pixiv.net/touch/ajax/user/illusts?id={id}'.format(id=str(id))
    img_ids = []
    proxies = get_proxies()
    headers = get_headers()
    res = requests.get(url, proxies=proxies, headers=headers)
    data = json.loads(res.content)
    try:
        illusts = data['body']['illusts']
        for illust in illusts:
            img_ids.append(illust['id'])
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
            count+=1
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
    print(img_urls)
    for img_url in img_urls:
        save_img(img_url)



if __name__ == '__main__':
    main()