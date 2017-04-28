"""
这个程序是为了统计活动汇集贴内所有的回复数, 用户需要输入合法的URL来进行计算, 输入 exit 退出

统计规则:
    1. 汇集贴的回复数也算在内
    2. 回复数是页面显示的回复数+1 (因为主题帖本身页算是一个回复)

注意事项:
    1. 运行环境为 Python3.5
    2. 需要安装 Requests, BeautifulSoup 模块
"""


# Requests 模块用来下载网页源代码
import requests
# BeautifulSoup4 模块用来解析网页源代码
from bs4 import BeautifulSoup
import re

POSTS_URL = 'http://36.01ny.cn/forum.php?mod=viewthread&tid=4448680&extra=page%3D1'
replies_number = 0


# 该函数需要输入一个用BeautifulSoup解析之后的变量, 返回帖子主题, 和该网页的回复数
def count_replies(f_url):
    # 抓去并解析传入的url
    f_html = requests.get(f_url)
    f_soup = BeautifulSoup(f_html.text, 'html.parser')
    # 获取回复数
    replies_num = int(f_soup.find('td', class_='pls ptn pbn').find_all('span', class_='xi1')[1].text) + 1
    # 获取帖子主题
    forum_topic = f_soup.find('span', id='thread_subject').text
    # 在Python语言中, 函数的多个返回值存在一个 Tuple 中
    return forum_topic, replies_num


# 程序进入无限循环, 输入有误提示重新输入, 输入exit退出程序
while True:
    replies_number = 0
    POSTS_URL = input('\n请输入汇集贴的链接 (输入exit退出): \n')
    # 这行代码纯粹是为了在PyCharm里面输入方便, 可以去掉后面的空格, 否则一按回车链接自动跳转
    POSTS_URL = POSTS_URL.split(' ')[0]
    if re.match('http://36.01ny.cn/', POSTS_URL):
        # 解析第一页
        html = requests.get(POSTS_URL)
        soup = BeautifulSoup(html.text, 'html.parser')

        # 打印出网页标题
        print()
        print('----------------------------------------------------------------------------------')
        print(soup.title.text.split(' ')[0], '\n')

        # 获取汇集贴中所有的活动链接(自动过滤掉其他链接)
        post = soup.find('td', class_='t_f')
        forums = post.find_all('a', href=re.compile(r'http://36.01ny.cn/'))

        # 汇集贴的回复数也计算在内
        replies_number += int(soup.find('td', class_='pls ptn pbn').find_all('span', class_='xi1')[1].text) + 1
        print('【汇集贴】: ')
        print(soup.find('span', id='thread_subject').text)
        print(POSTS_URL, ':', replies_number, '回复')
        print()

        # 深入到每个活动帖中, 统计每一个活动帖的回复数, 并累加
        print('【活动贴】: 共', len(forums), '主题贴')
        for forum in forums:
            forum_url = forum['href']
            # 对函数返回值的 Tuple 进行解包
            (forum_name, forum_count) = count_replies(forum_url)
            replies_number += forum_count
            print(forum_name)
            print(forum_url, ':', forum_count, '回复')

        # 打印出最终结果
        print('\n总计:', replies_number, '回复')
        print('----------------------------------------------------------------------------------')
    elif POSTS_URL == 'exit':
        print('谢谢使用, 再见!')
        break
    else:
        print('输入的链接不合法, 请检查格式!')
        continue
