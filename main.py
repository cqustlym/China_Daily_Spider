import requests
from time import sleep
from bs4 import BeautifulSoup
headers = {
    'Accept': "application/json, text/plain, */*",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
}

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接


# 每次运行读取txt文件，看内容是否已经抓取过，如果抓过则忽略。
f = open( 'existing_list.txt', 'r' )
title_list = f.readline().split('#')
f.close()

title_list_links = []
url = 'https://language.chinadaily.com.cn/news_bilingual/'
response = requests.get(url,headers=headers,timeout=300)
soup = BeautifulSoup(response.text,'lxml')
items = soup.select('body > div.content > div.content_left > div > div > p.gy_box_txt2 > a')
for title,link in zip(items,items):
    data = {
        'title':title.get_text(),
        'link':link.get('href')[2:]
    }
    if data['title'] not in title_list:
        sleep(2) # 防止被ban
        print(f"正在下载 {data['title']} .......")
        response = requests.get('https://' + data['link'],headers=headers,timeout=300)
        soup = BeautifulSoup(response.text,'lxml')
        content = soup.select('#Content > p')
        date = soup.select('#syno-nsc-ext-gen3 > div.content > div.content_left > div.main > div.main_title > p')
        f = open( 'existing_list.txt', 'a' )
        f.write(data['title'] + '#')
        g = open( data['title']+ '.txt', 'a' ) #日期+标题
        for i in content:
            g.write(i.get_text())
            g.write('\n''\n')
print('Done!')
f.close()
g.close()