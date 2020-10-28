from common import vgg_model_init
from vggnet import VGGNet
import numpy as np
from milvus import Milvus, IndexType, MetricType
import os


#初始化VGG模型
model,graph = vgg_model_init.load_model()

#读取图片路径
def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if (f.endswith('.jpg') or f.endswith('.png'))]

#提取特征
def feature_extract(database_path, model):
    feats = []
    names = []
    img_list = get_imlist(database_path)
    model = model
    for i, img_path in enumerate(img_list):
        norm_feat = model.vgg_extract_feat(img_path)
        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name.encode())
        current = i+1
        total = len(img_list)
        print ("extracting feature from image No. %d , %d images in total" %(current, total))
    return feats, names

if __name__ == '__main__':
    # feats,names = feature_extract("img/test2", VGGNet())
    # feats = np.array(feats)

    # 初始化一个Milvus类，以后所有的操作都是通过milvus来的
    milvus = Milvus(host='49.235.115.64',port='19530')
    # print(feats.shape)
    # for feat in feats:
    #     print(feat)
