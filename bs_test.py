from bs4 import BeautifulSoup

def find_class():
    soup = BeautifulSoup(open('鬼.html', encoding='utf-8'), 'html.parser')
    a = soup.find_all('a')
    print(a)

find_class()