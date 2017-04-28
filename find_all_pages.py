# Requests 模块涌来下载网页源代码
import requests
# BeautifulSoup4 模块用来解析网页源代码
from bs4 import BeautifulSoup
import re


# 定义一个函数用来下载Image
def saveImage(imgUrl, imgName='default.jpg', path='/Users/hayden/Desktop/影赛/'):
    response = requests.get(imgUrl, stream=True)
    imagex = response.content
    print('保存文件' + path + imgName + '\n')
    try:
        with open(path + imgName, 'wb') as jpg:
            jpg.write(imagex)
            return
    except IOError:
        print('IO Error\n')
        return
    finally:
        print('保存完成')
        # jpg.close()



CONTEST_URL = 'http://36.01ny.cn/forum.php?mod=viewthread&tid=4442519'


# 网页管理器: 存储影赛栏目下所有参赛的帖子
xxhtml = requests.get(CONTEST_URL)
xxsoup = BeautifulSoup(html.text, 'html.parser')


images = soup.find_all('img', class_='zoom')

number_of_image = len(images)
name = 'xxxxx'
image_path = '/Users/hayden/Desktop/影赛/'
index = 1
for image in images:
    print(image['file'])
    image_url = image['file']
    if number_of_image == 1:
        image_name = name + '.jpg'
        saveImage(image_url, image_name, image_path)
    else:
        image_name = name + '-' + str(index) + '.jpg'
        saveImage(image_url, image_name, image_path)
        index += 1







