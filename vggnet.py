import os

import numpy as np
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
from keras.preprocessing import image
from numpy import linalg as LA
from common.const import input_shape
import time


# 读取图片路径
def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if (f.endswith('.jpg') or f.endswith('.png'))]

class VGGNet:
    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model_vgg = VGG16(weights=self.weight,
                               input_shape=(self.input_shape[0], self.input_shape[1], self.input_shape[2]),
                               pooling=self.pooling,
                               include_top=False)
        self.model_vgg.predict(np.zeros((1, 224, 224, 3)))

    def vgg_extract_feat(self, img_path):
        img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_vgg(img)
        feat = self.model_vgg.predict(img)
        #归一化
        norm_feat = feat[0] / LA.norm(feat[0])
        norm_feat = [i.item() for i in norm_feat]
        return norm_feat

    def vgg_extract_feat_batch(self, img_path):
        imgs = []
        norm_feats = []
        names = []
        img_list = get_imlist(img_path)
        for i,pa in enumerate(img_list):
            img = image.load_img(pa, target_size=(self.input_shape[0], self.input_shape[1]))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input_vgg(img)
            imgs.append(img)
            img_name = os.path.split(pa)[1]
            names.append(img_name.encode())
        imgs = np.concatenate([x for x in imgs])
        feats = self.model_vgg.predict(imgs,batch_size=32)
        # print(feats)
        count = 0
        for feat in feats:
            count += 1
            norm_feat = feat / LA.norm(feat)
            norm_feat = [i.item() for i in norm_feat]
            norm_feats.append(norm_feat)
        return norm_feats, names

#提取图片特征
def vgg_extract_feat(img_path, model, graph, sess):
    with sess.as_default():
        with graph.as_default():
            img = image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input_vgg(img)
            feat = model.predict(img)
            norm_feat = feat[0] / LA.norm(feat[0])
            norm_feat = [i.item() for i in norm_feat]
            return norm_feat



if __name__ == '__main__':
    path = 'tmp/keyframe/kexuejia'
    vgg = VGGNet()
    feats_list = []
    # start = time.clock()
    # img_list = get_imlist(path)
    # for i, img_path in enumerate(img_list):
    #     norm_feat = vgg.vgg_extract_feat(img_path)
    #     feats_list.append(norm_feat)
    #     # print(norm_feat)
    # print(time.clock() - start)
    print("-------------------------------------------------------------------------------------")
    start1 = time.clock()
    feats = vgg.vgg_extract_feat_batch(path)
    print(time.clock() - start1)