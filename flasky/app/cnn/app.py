#!/usr/bin/env python3
# coding=utf-8

import json, argparse, time

import tensorflow as tf
from load import load_graph

from flask import Flask, request
from flask_cors import CORS

from tensorflow_cnn_train import crack_captcha

##################################################
# API part
##################################################
app = Flask(__name__)
cors = CORS(app)

import os
import numpy as np
base_dir = os.path.abspath(os.getcwd())
print(base_dir)
captcha_path = '/Users/alpha/github/Flask/flasky/app/static/captcha.jpg'

# 把彩色图像转为灰度图像（色彩对识别验证码没有什么用）
def convert2gray(img):
    if len(img.shape) > 2:
        gray = np.mean(img, -1)
        # 上面的转法较快，正规转法如下
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img

# 向量转回文本
def vec2text(vec):
    char_pos = vec.nonzero()[0]
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i  # c/63
        char_idx = c % 57
        if char_idx < 10:
            char_code = char_idx + ord('0')
        elif char_idx < 36:
            char_code = char_idx - 10 + ord('A')
        elif char_idx < 62:
            char_code = char_idx - 36 + ord('a')
        elif char_idx == 62:
            char_code = ord('_')
        else:
            raise ValueError('error')
        text.append(chr(char_code))
    return "".join(text)


@app.route("/api/predict", methods=['POST'])
def predict():
    start = time.time()

    data = request.data.decode("utf-8")
    if data == "":
        params = request.form
        x_in = json.loads(params['x'])
    else:
        params = json.loads(data)
        x_in = params['x']

    ##################################################
    # Tensorflow part
    ##################################################
    y_out = persistent_sess.run(y, feed_dict={
        x: x_in
        # x: [[3, 5, 7, 4, 5, 1, 1, 1, 1, 1]] # < 45
    })
    ##################################################
    # END Tensorflow part
    ##################################################

    json_data = json.dumps({'y': y_out.tolist()})
    print("Time spent handling the request: %f" % (time.time() - start))

    return json_data


@app.route('/api/test/')
def predict_test():
    # return '测试cnn'
    from PIL import Image
    image = Image.open(captcha_path)
    image = np.array(image)
    image = convert2gray(image)  # 生成一张新图
    image = image.flatten() / 255  # 将图片一维化
    print('shape:', image.shape)

    # predict = tf.argmax(tf.reshape(y, [-1, 4, 57]), 2)
    # text_list = persistent_sess.run(predict, feed_dict={x: [image], keep_prob: 1})

    predict = crack_captcha(persistent_sess, x, image)
    print(predict)



##################################################
# END API part
##################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen_model_filename", default="results/frozen_model.pb", type=str,
                        help="Frozen model file to import")
    parser.add_argument("--gpu_memory", default=.2, type=float, help="GPU memory per process")
    args = parser.parse_args()

    ##################################################
    # Tensorflow part
    ##################################################
    print('Loading the model')
    # graph = load_graph(args.frozen_model_filename)
    # x = graph.get_tensor_by_name('prefix/Placeholder/inputs_placeholder:0')
    # y = graph.get_tensor_by_name('prefix/Accuracy/predictions:0')

    graph = load_graph('/Users/alpha/github/flask/flasky/app/cnn/model/frozen_model.pb')
    x = graph.get_tensor_by_name('prefix/inputs_placeholder:0')
    y = graph.get_tensor_by_name('prefix/predictions:0')
    keep_prob = graph.get_tensor_by_name('prefix/keep_prob:0')
    print(x, y, keep_prob)

    # X = tf.placeholder(tf.float32, [None, 60 * 160])
    # Y = tf.placeholder(tf.float32, [None, 4 * 57])
    # keep_prob = tf.placeholder(tf.float32)

    print('Starting Session, setting the GPU memory usage to %f' % args.gpu_memory)
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_memory)
    sess_config = tf.ConfigProto(gpu_options=gpu_options)
    persistent_sess = tf.Session(graph=graph, config=sess_config)
    ##################################################
    # END Tensorflow part
    ##################################################

    print('Starting the API')
    app.run(debug=False, port=8080)