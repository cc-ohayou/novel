# -*- coding:utf-8 -*-
import random
import time
from urllib import request
from bs4 import BeautifulSoup
import sys
import requests

#   bs4安装 参考博客 https://www.cnblogs.com/yysbolg/p/9040649.html
# >pip3 install Beautifulsoup4  >pip3 install lxml


class ShowProcess():
    i = 0
    max_steps = 0
    max_arrow = 50
    infoDone = 'done'

    def __init__(self, max_steps, infoDone='Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps)
        num_line = self.max_arrow - num_arrow
        percent = self.i * 100.0 / self.max_steps
        process_bar = '正在下载：' + chapter_name + '    总进度' + '[' + '>' * num_arrow + '-' * num_line + ']' \
                      + '%.2f' % percent + '%          ' + '\r'
        sys.stdout.write(process_bar)
        sys.stdout.flush()
        print(process_bar)
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0


def download_specified_chapter(textName, chapter_url, header, proxies, coding, chapter_name=None):
    download_req = request.Request(chapter_url, headers=header)
    # # 发送请求
    response = request.urlopen(download_req)
    download_html = response.read().decode(coding, 'ignore')
    origin_soup = BeautifulSoup(download_html, 'lxml')
    content = origin_soup.find(class_='panel-body content-body content-ext')
    txt = content.text.replace('\xa0' * 8, '')
    txt = txt.replace('\n\n', '\n')
    txt = txt.replace('七-三*小说__网  www.73x s.cc', '')
    txt = txt.replace('七!三)(小@#说网  www.7 3xs.cc', '')
    with open(textName, "a", encoding='utf-8') as f:
        if chapter_name is None:
            f.write('\n')
        else:
            f.write('\n' + chapter_name + '\n')
        f.write(txt)


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    print(proxies)
    return proxies


def get_random_ip_proxies():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    return get_random_ip(ip_list)


if __name__ == "__main__":
    print("获取章节中")
    index_url = "http://www.yishengchuancheng.com/i78579/"
    commonUrl = "http://www.yishengchuancheng.com/"
    firstChapterName = '第459章 隐居南华城'
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/'
                      '535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    }
    url_req = request.Request(index_url, headers=header)
    response = request.urlopen(url_req)
    html = response.read().decode('gbk', 'ignore')
    html_soup = BeautifulSoup(html, 'lxml')
    index = BeautifulSoup(str(html_soup.find_all('ul', class_='list-group list-charts')), 'lxml')
    print("获取章节完成，开始下载：")
    body_flag = False
    max_steps = 2489
    process_bar = ShowProcess(max_steps, 'OK')
    chapters = index.find_all(['li'])
    print(str(type(chapters)) + ',' + str(len(chapters)))
    proxies=get_random_ip_proxies()
    for element in chapters:
        if element.string == firstChapterName:
            body_flag = True
        if body_flag is True and element.name == 'li':
            time.sleep(1)
            chapter_name = element.string
            chapter_url = commonUrl + element.a.get('href')
            download_specified_chapter('最强仙帝.txt', chapter_url, header, proxies,'gbk', chapter_name)
            process_bar.show_process()
    print("下载完成")
