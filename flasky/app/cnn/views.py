import os
from flask import render_template, redirect, url_for
from PIL import Image
import numpy as np
from . import cnn
from tensorflow_cnn_train import convert2gray, crack_captcha
from gen_captcha import gen_captcha_text_and_image
import tensorflow as tf

base_dir = os.path.abspath(os.getcwd())
print(base_dir)
captcha_path = os.path.join(base_dir, 'app/static/captcha.jpg')


@cnn.route('/cnn/')
def cnn_index():
    import base64    
    with open(captcha_path,"rb") as f:
        # b64encode是编码，b64decode是解码  
        base64_data = base64.b64encode(f.read()).decode()
        # base64.b64decode(base64data)  
        print(base64_data)
    return render_template('cnn.html', base64_data=base64_data)


@cnn.route('/cnn/predict/')
def cnn_predict():
    # text, image = gen_captcha_text_and_image()
    # image = Image.fromarray(image)
    # captcha_image = Image.open(captcha_path)
    # # image = np.array(captcha_image)
    # # image = convert2gray(image)  # 生成一张新图
    # # image = image.flatten() / 255  # 将图片一维化
    # # predict_text = crack_captcha(image)  # 导入模型识别
    # # return "预测结果结果是: {}".format(predict_text)
    # text, image = gen_captcha_text_and_image()
    # print(text)
    # image = convert2gray(image)  # 生成一张新图
    # print(image)
    # image = image.flatten() / 255  # 将图片一维化
    # predict_text = crack_captcha(image)  # 导入模型识别
    # print("正确: {}  预测: {}".format(text, predict_text))
    # return "正确: {}  预测: {}".format(text, predict_text)
    image = Image.open(captcha_path)
    image = np.array(image)
    image = convert2gray(image)  # 生成一张新图
    image = image.flatten() / 255  # 将图片一维化
    print(image)
    predict_text = crack_captcha(image)  # 导入模型识别
    return "预测结果结果是: {}".format(predict_text)


@cnn.route('/cnn/random/')
def cnn_random():
    text, image = gen_captcha_text_and_image()
    image = Image.fromarray(image)
    image.save(captcha_path)
    return redirect(url_for('cnn.cnn_index'))


if __name__ == '__main__':
    path = '/Users/alpha/github/Flask/flasky/app/static/captcha.jpg'
    captcha_image = Image.open(path)
    image = np.array(captcha_image)
    image = convert2gray(image)  # 生成一张新图
    image = image.flatten() / 255  # 将图片一维化
    predict_text = crack_captcha(image)  # 导入模型识别
    print("预测结果结果是: {}".format(predict_text))

