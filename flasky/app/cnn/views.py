import os
from flask import render_template, redirect, url_for, session
from PIL import Image
import numpy as np
from . import cnn
from tensorflow_cnn_train import convert2gray, crack_captcha, vec2text
from gen_captcha import gen_captcha_text_and_image
import tensorflow as tf

# from .load import graph, x, y, keep_prob, persistent_sess

base_dir = os.path.abspath(os.getcwd())
print(base_dir)
captcha_path = os.path.join(base_dir, 'app/static/captcha.jpg')
saver = None


@cnn.route('/cnn/')
def cnn_index():
    import base64
    with open(captcha_path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read()).decode()
        # base64.b64decode(base64data)
        print(base64_data)
    return render_template('cnn.html', base64_data=base64_data)


# @cnn.route('/cnn/predict/')
# def cnn_predict():
#     from PIL import Image
#     image = Image.open(captcha_path)
#     image = np.array(image)
#     image = convert2gray(image)  # 生成一张新图
#     image = image.flatten() / 255  # 将图片一维化
#     print('shape:', image.shape)
#
#     # predict = tf.argmax(tf.reshape(y, [-1, 4, 57]), 2)
#     # text_list = persistent_sess.run(predict, feed_dict={x: [image], keep_prob: 1})
#
#     out_put = graph.get_tensor_by_name("prefix/out_put:0")
#     predict = tf.argmax(tf.reshape(out_put, [-1, 4, 63]), 2)
#     text_list = persistent_sess.run(predict, feed_dict={x: [image], keep_prob: 1})
#     text = text_list[0].tolist()
#     vector = np.zeros(4 * 63)
#     i = 0
#     for n in text:
#         vector[i * 63 + n] = 1
#         i += 1
#     print(vec2text(vector))
#     return vec2text(vector)

@cnn.route('/cnn/predict/')
def cnn_predict():
    from PIL import Image

    image = Image.open(captcha_path)
    image = np.array(image)
    image = convert2gray(image)  # 生成一张新图
    image = image.flatten() / 255  # 将图片一维化
    model_path = '/Users/alpha/github/model/'
    predict_text = crack_captcha(image, model_path)
    return predict_text


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

