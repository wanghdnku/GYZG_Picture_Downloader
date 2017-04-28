"""
该程序是为了统计影赛信息编写, 该程序可以自动下载影赛图片到指定位置, 并生成统计影赛信息的Excel文件.

在程序中, 用户需要输入:
    1. 影赛板块的URL: 如 'http://36.01ny.cn/forum.php?mod=forumdisplay&fid=1187'
    2. 希望存储照片的位置: 如 '/Users/hayden/Desktop/影赛/' (Windows和MacOS下文件的路径不同,请务必输入正确, 并在最后加上'/')
    3. 影赛板块是是否有置顶的征稿启事: 如果有输入Y, 程序会自动去掉第一个帖子; 如果没有, 输入N

注意事项:
    1. 运行环境为 Python3.5
    2. 需要安装 Requests, BeautifulSoup模块
"""


# Requests 模块用来下载网页源代码
import requests
# BeautifulSoup4 模块用来解析网页源代码
from bs4 import BeautifulSoup
# 使用正则表达式
import re
# 读写csv文件
import csv


# 定义一个函数用来下载Image
def saveImage(imgUrl, imgName='default.jpg', path='/Users/hayden/Desktop/影赛/'):
    response = requests.get(imgUrl, stream=True)
    raw_image = response.content
    # print('保存文件' + path + imgName + '\n')
    try:
        with open(path + imgName, 'wb') as jpg_file:
            jpg_file.write(raw_image)
            return
    except IOError:
        print(' ---- IO错误: 请检查文件路径!\n')
        return
    finally:
        print(' ---- 保存图片 ' + path + imgName + ' 成功')


# CONTEST_URL = 'http://36.01ny.cn/forum.php?mod=forumdisplay&fid=1187'
# STORAGE_PATH = '/Users/hayden/Desktop/影赛/'

# 表示帖子有几页
pageNumber = 0
# 表示着是否存在征稿启事
hasNotice = False
# 一个字典,用来存储所有的帖子(字典不允许有键值相同的项目存在)
postList = dict()

# 从控制台输入影赛链接, 存储位置, 以及是否有征稿启事
# 存储影赛页面的URL
CONTEST_URL = input('请输入影赛的链接: ')
# 这行代码纯粹是为了在PyCharm里面输入方便, 可以去掉后面的空格, 否则一按回车链接自动跳转
CONTEST_URL = CONTEST_URL.split(' ')[0]
# 照片希望存储的位置(文件夹必须事先存在)
STORAGE_PATH = input('请输入文件夹路径: ')
STORAGE_PATH_NAMELESS = input('请输入匿名图片文件夹路径: ')

# 测试使用
#CONTEST_URL = 'http://36.01ny.cn/forum.php?mod=forumdisplay&fid=1204'
#STORAGE_PATH = '/Users/hayden/Desktop/contest/'
#STORAGE_PATH_NAMELESS = '/Users/hayden/Desktop/contest_nameless/'

notice = input('第一页是否有置顶的汇集贴? (Y/N): ')
if notice == 'Y' or notice == 'y':
    hasNotice = True
elif notice == 'N' or notice == 'n':
    hasNotice = False
else:
    print('输入有误, 系统默认为Y')
    hasNotice = True


# 解析第一页
html = requests.get(CONTEST_URL)
soup = BeautifulSoup(html.text, 'html.parser')

# 打印出网页标题
print('\n')
print(soup.title.text, '\n')

# 利用正则表达式匹配'共x页', 解析出总共的页数, 并存储在pageNumber中
links = soup.find_all('span', title=re.compile(r'\u5171 \d+ \u9875'))

# 只有一页的话, 网页不显示'共x页', 所以links将为空列表
if not links:
    pageNumber = 1
else:
    pageNumber = int(links[0].text.split(' ')[2])
print('本影赛共有', pageNumber, '页主题帖\n')


log = {}

# 将每一页中的帖子全部解析出来
pageIndex = 1
while pageNumber > 0:

    postPage = CONTEST_URL + '&page=' + str(pageIndex)
    print('开始解析第', pageIndex, '页: ', postPage)
    # print(postPage)
    pageHtml = requests.get(postPage)
    pageSoup = BeautifulSoup(pageHtml.text, 'html.parser')

    # 获取所有的Posts。根据窗口大小来判断是不是帖子。
    posts = pageSoup.find_all('li', style='width:227px')

    # 如果是第一页, 并且存在置顶的'征稿启事'贴的话, 删去该帖子
    if pageIndex == 1 and hasNotice:
        posts.pop(0)

    print(' ---- 本页共有', len(posts), '个主题帖')

    # 遍历所有的参赛贴, 并存储在一个字典类型中
    for post in posts:

        # 解析发帖人的网名和ID
        # 网页改版，此处发生变化
        author = post.contents[7].find_all('a')[1]
        authorName = author.text
        authorId = author['href'].split('uid-')[1].split('.html')[0]

        # 解析帖子的名称和ID
        topic = post.contents[1].find('a')
        topicName = topic['title']
        topicId = topic['href'].split('thread-')[1].split('-1-')[0]

        # 拼接出"只显示楼主"的新帖子URL
        topicURL = 'http://36.01ny.cn/forum.php?mod=viewthread&tid=' + topicId + '&page=1&authorid=' + authorId
        photoName = '《' + topicName + '》---' + authorName

        # 写入日志
        log[topicURL] = 'Page ' + str(pageIndex)

        # 把信息保存在字典中(字典可以去重), 统一发帖人发重复的名字将被删去
        postList[photoName] = topicURL

    pageIndex += 1
    pageNumber -= 1

# print(dictionary)
print('\n======== 开始下载影赛图片 ========\n')

# 在内存中创建一个Excel文件, 并创建一个'影赛统计'表
#wb = xlwt.Workbook()
#ws = wb.add_sheet('影赛统计')
row = 0

csv_path = STORAGE_PATH + 'Info.csv'
csv_file = open(csv_path, 'w', encoding='gbk')
writer = csv.writer(csv_file)

# 再生成一份匿名的文件
csv_path_nameless = STORAGE_PATH_NAMELESS + 'Info_nameless.csv'
csv_file_nameless = open(csv_path_nameless, 'w', encoding='gbk')
writer_nameless = csv.writer(csv_file_nameless)

# 遍历整个字典, 下载每个帖子里的照片, 并写入到Excel中去.
for (name, url) in postList.items():
    # 向主题帖内部进军!!!!
    print('参赛作品:', name)
    print('帖子链接:', url)

    # 网页管理器: 存储影赛栏目下所有参赛的帖子
    image_html = requests.get(url)
    image_soup = BeautifulSoup(image_html.text, 'html.parser')

    images = image_soup.find_all('img', class_='zoom', file=re.compile(r'http://f.01ny.cn/'))

    number_of_image = len(images)
    image_path = STORAGE_PATH
    index = 1

    nameless = name.split('---')[0]
    image_path_nameless = STORAGE_PATH_NAMELESS

    # 遍历一个主题帖中的所有图片
    for image in images:
        image_url = image['file']
        if number_of_image == 1:
            # 存储照片
            image_name = str(row+1) + '.' + name + '.jpg'
            saveImage(image_url, image_name, image_path)
            # 存储匿名照片
            image_nameless = str(row + 1) + '.' + nameless + '.jpg'
            saveImage(image_url, image_nameless, image_path_nameless)
        else:
            # 存储照片
            image_name = str(row+1) + '.' + name + '-' + str(index) + '.jpg'
            saveImage(image_url, image_name, image_path)
            # 存储匿名照片
            image_nameless = str(row + 1) + '.' + nameless + '-' + str(index) + '.jpg'
            saveImage(image_url, image_nameless, image_path_nameless)
            index += 1

    log[url] = 'Done'

    # 存完一个主题帖后换行, 将主题帖信息写入Excel文件中
    print()

    # 写入csv
    writer.writerow([str(row + 1), str(name.split('---')[0]), str(name.split('---')[1])])
    writer_nameless.writerow([str(row + 1), str(name.split('---')[0])])

    row += 1


with open(STORAGE_PATH + 'log.txt', 'w') as logFile:
    for (url, status) in log.items():
        logFile.write(url + '\t\t' + status + '\n')

# 全部统计完之后, 在制定路径存储Excel文件
csv_file.close()
csv_file_nameless.close()
print('文件存储完毕! ')
