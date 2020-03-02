'''
本程序实现可在  笔趣看（https://www.biqukan.com/） 网站爬取小说所有内容并下载到本地指定位置指定的文件（.txt）内,由于使用单线程所以速度较慢。
使用方法：
        1.运行程序后输入要下载的笔趣看小说的章节目录网页地址（例如：https://www.biqukan.com/0_790/）回车若跳转网页则把'/'删除重新打一个'/'再回车即可
        2.然后下载文件的命名（例如：元尊）
        3.输入想要下载到的地址（例如：F:\）
        回车后程序就会开始下载并显示当前下载百分比，速度较慢。
'''

import requests
from bs4 import BeautifulSoup
import sys


class downloader(object):
    def __init__(self):
        self.server = 'https://www.biqukan.com'
        self.html = input('请输入网址：')
        self.names = []  # 章节名
        self.urls = []  # 章节地址
        self.num = 0  # 章节数
        self.bookname = input('请输入生成txt文件的名称：')  # 文件的名称
        self.path = input('请输入文件下载路径')  # 文件的下载路径

    def get_information(self):
        html_all = requests.get(url=self.html)
        html_all.encoding = 'GBK'
        html_x=html_all.text
        html = BeautifulSoup(html_x)
        url_all_not = html.find_all('div', class_='listmain')
        url_all = BeautifulSoup(str(url_all_not[0]))
        url = url_all.find_all('a')
        self.num = len(url[12:])
        for i in url[12:]:
            self.names.append(i.string)
            self.urls.append(self.server + i.get('href'))

    def get_content(self, html):
        html_a = requests.get(url=html)
        html_a.encoding='GBK'
        html_x=html_a.text
        html_b = BeautifulSoup(html_x)
        book = html_b.find_all('div', class_='showtxt')
        book_txt = book[0].text
        return book_txt

    def write(self):
        try:
            for i in range(self.num):
                with open(self.path+'/'+self.bookname+'.txt','a', encoding='utf-8') as a:
                    a.write(self.names[i] + '\n')
                    a.writelines(self.get_content(self.urls[i]))
                    a.write('\n\n')
                    sys.stdout.write(f'已下载：{i / self.num}%....')
                    sys.stdout.flush()
        except FileNotFoundError:
            print('输入的地址无效，请重新输入')
            path = input('请输入新的地址：')
            self.path = path
            self.write()
        finally:
            print('下载完成！')


if __name__ == '__main__':
    d = downloader()
    d.get_information()
    print('开始下载')
    d.write()
