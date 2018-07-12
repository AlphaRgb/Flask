import os
from gen_captcha import gen_captcha_text_and_image
from gen_captcha import number
from gen_captcha import alphabet
from gen_captcha import ALPHABET

import numpy as np
import tensorflow as tf

text, image = gen_captcha_text_and_image()
print("验证码图像channel:", image.shape)  # (60, 160, 3)
# 图像大小
IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
IMAGE_CHANNEL = 3
MAX_CAPTCHA = len(text)
print("验证码文本最长字符数", MAX_CAPTCHA)


class TFCNNTrainer:
    CHAR_SET_LEN = number + alphabet + ALPHABET + ['_']
    base_model_dir = './model/'

    def __init__(self, capType, height=60, width=200, channel=3, max_captcha=4):
        super(TFCNNTrainer, self).__init__()
        self.capType = capType
        self.IMAGE_HEIGHT = height
        self.IMAGE_WIDTH = width
        self.IMAGE_CHANNEL = channel
        self.MAX_CAPTCHA = max_captcha
        self.model_dir = os.path.join(TFCNNTrainer.base_model_dir, capType)
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
        self.has_check_point = True if os.path.exists(os.join(self.model_dir, 'checkpoint')) else False
        pass

    # 有时生成图像大小不是(60, 160, 3)
    def wrap_gen_captcha_text_and_image(self):
        while True:
            text, image = gen_captcha_text_and_image()
            if image.shape == (self.IMAGE_HEIGHT, self.IMAGE_WIDTH, self.IMAGE_CHANNEL):
                return text, image