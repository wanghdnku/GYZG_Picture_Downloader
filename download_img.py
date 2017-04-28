import requests


def saveImage(imgUrl, imgName="default.jpg"):
    response = requests.get(imgUrl, stream=True)
    image = response.content
    imagePath = "/Users/hayden/Desktop/影赛/"
    print("保存文件" + imagePath + imgName + "\n")
    try:
        with open(imagePath+imgName, "wb") as jpg:
            jpg.write(image)
            return
    except IOError:
        print("IO Error\n")
        return
    finally:
        print('done')
        # jpg.close()


saveImage('http://f.01ny.cn/forum/201605/23/230413h7yn77ne7xbi7brx.jpg', 'xxxxx.jpg')