import requests
from config_reader import get_headers
rawcookies = '_iuqxldmzr_=32; _ntes_nnid=9b610f53837336f5e278b9f432950d52,1565266261067; _ntes_nuid=9b610f53837336f5e278b9f432950d52; WM_TID=tPMQ64kyGIFFAQVVUBNt4CsHTB7fsoIi; __oc_uuid=5192c4f0-da9b-11e9-af11-77c570ec3654; UM_distinctid=1708c47b38d8bf-0e452674ffed81-4313f6b-16e360-1708c47b38e79c; vinfo_n_f_l_n3=1d756b383e6aa1c3.1.0.1582901473264.0.1582901477556; WM_NI=v5zFq6fy35lxZySX5sscEOjxUvkEHPyrP1uO1KkENGf7gsc2AuT%2BVIOMRzY8q47mElsCgl6g%2FFHNHQOV3kR91dcKCt8O2sdn62tNj9Knp6TJlNCvLOyrqlK7vMS%2FGw91ajU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeaac762f88ce590c44ab4b88ea2c55e839a9aabaa4b948bae9bd350bc8c9d86d72af0fea7c3b92ab6ebb6a7f43ea6a7fdd6ef749aa79db9b879b1bd8bb0e97497aaa5a6cb5cbbaea0d2f845f395a5a6cd4da6e9a994e23a83ab9cccd5438d939e9bdc34b3ecf98ec868b19da98db56ded9a88afcb5b8d8afd8cd133f3bcadacc280fc91fe94e766f6eebcafe93389b2c0d7d742b0928d97cf45bbaebf8dca3db6939dd0c67dfbefaf8bd837e2a3; JSESSIONID-WYYY=8Q4JrlxST0J20yxx9GMSqJ7t7zmKvXMuOI%5C%2B35YmKMP%2B0w%5CR%2Frn4dXZs33iN%5C1XPmKwF%5CtPSSMz%5CUpDF1uz4oD25VKbzw0eeO2zQY3M5T876c53dDExoFHd1pCMwDoDa0bPdoZi73cOG8cssymrlJG80JYZDIdtExUYcxYV3UNq%2BlEWz%3A1583839122794; __remember_me=true; ntes_kaola_ad=1; MUSIC_U=52ef9c5b109988fb3831e80bceefbebf3126a85ac0c8e662ba9393a9af3d7c6a2c1cae514e37debcc04b4eb47b726cba41049cea1c6bb9b6; __csrf=28d4ef275283ab6250e22a40f1880441'


def cookie_parse():
    cookies = {}
    for line in rawcookies.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    return cookies


def pa():
    cookies = cookie_parse()
    url = 'https://music.163.com/#/my/m/music/playlist?id=81348911'
    res = requests.get(url, cookies=cookies, headers=get_headers())
    print(res.status_code)
    print(res.content)
    with open('鬼.html', 'wb') as f:
        f.write(res.content)


pa()