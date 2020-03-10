from configparser import ConfigParser
import abandoned


def set_config(cookies):
    config = ConfigParser()
    config['cookies'] = cookies
    with open('config.ini', 'a+', encoding='unicode') as file:
        config.write(file)
    return


def get_proxies():
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['proxies']


def get_img_dir():
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['files']['img_dir']


def get_headers():
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config['headers']