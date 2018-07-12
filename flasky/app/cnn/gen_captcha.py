#!/usr/bin/env python3
# coding=utf-8

import os
from captcha.image import ImageCaptcha  # pip install captcha
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from PIL import Image
import random

# 验证码中的字符, 就不用汉字了
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=number + alphabet + ALPHABET, captcha_size=4):
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    image = ImageCaptcha()

    # 此处只训练只有小写字母的结果
    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text)

    captcha = image.generate(captcha_text)

    # # 存储文件使用
    # base_dir = os.path.abspath(os.path.dirname(__file__))
    # files_dir = os.path.abspath(os.path.join(os.getcwd(), '../static'))
    # print(files_dir)
    # image_dir = os.path.join(files_dir, 'captcha.jpg')
    #
    # image.write(captcha_text, image_dir)

    # 生成训练文件
    captcha_image = Image.open(captcha)
    # captcha_image.show()
    captcha_image = np.array(captcha_image)
#    print(captcha_image)
    return captcha_text, captcha_image


# 随机生成一张验证码
def gen_captcha_image_random():
    image = ImageCaptcha()

    captcha_text = random_captcha_text()
    captcha_text = ''.join(captcha_text)

    captcha = image.generate(captcha_text)
    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image)
    print(captcha_image)


def test_array_image():
    text, image = gen_captcha_text_and_image()
    image = Image.fromarray(image)
    print(text, image)
    path = '/Users/alpha/github/Flask/flasky/app/static/captcha.jpg'
    image.save(path)



if __name__ == '__main__':
    # 测试
    # text, image = gen_captcha_text_and_image()
    # gen_captcha_text_and_image()
    # gen_captcha_image_random()
    # f = plt.figure()  # 图
    # ax = f.add_subplot(111)  # 坐标轴,参数111的意思是:将画布分割成1行1列，图像画在从左到右从上到下的第1块
    # # transform=ax.transAxes这句话是为了说明坐标轴是以axes坐标系为标准的，(0,0)就是axes的左下角，(1,1)是右上角
    # ax.text(0.1, 0.9, text, ha='center', va='center', transform=ax.transAxes)
    # # plt.imshow()函数负责对图像进行处理，并显示其格式，而plt.show()则是将plt.imshow()处理后的函数显示出来
    # plt.imshow(image)
    # plt.show()
    test_array_image()
