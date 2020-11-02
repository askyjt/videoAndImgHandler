from common import vgg_model_init, const
import numpy as np
import milvus_util
import os

# 初始化VGG模型
from vggnet import VGGNet

model, graph, sess = vgg_model_init.load_model()


# 读取图片路径
def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if (f.endswith('.jpg') or f.endswith('.png'))]


# 提取特征
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
        current = i + 1
        total = len(img_list)
        print("extracting feature from image No. %d , %d images in total" % (current, total))
    return feats, names


# 将特征存入milvus
def save_feature(feats, table_name):
    client = milvus_util.milvus_client()
    status, feats_ids = milvus_util.insert_vectors(client=client, table_name=table_name, vectors=feats)
    return feats_ids


# 通过图片查询视频或图片
def search_video_or_img(img_path, table_name, top_k=10):
    client = milvus_util.milvus_client()
    feats = []
    norm_feat = model.vgg_extract_feat(img_path=img_path)
    feats.append(norm_feat)
    status, res = milvus_util.search_vectors(client=client, table_name=table_name, vectors=feats, top_k=top_k)
    return status, res


def save_video_to_milvus(keyframe_path):
    feats = []
    norm_feat = model.vgg_extract_feat(img_path=keyframe_path)
    feats.append(norm_feat)
    feats_ids = save_feature(feats=feats, table_name='video')
    return feats_ids


if __name__ == '__main__':
    # feats,names = feature_extract("img/test2", VGGNet())
    # feats = np.array(feats)

    # 初始化一个Milvus类，以后所有的操作都是通过milvus来的
    # milvus = Milvus(host='49.235.115.64',port='19530')

    # print(feats.shape)
    # for feat in feats:
    #     print(feat)

    # 创建连接
    table_name = 'test1'
    feats, names = feature_extract("img/test1", VGGNet())
    client = milvus_util.milvus_client()
    # milvus_util.create_table(client=client, table_name=table_name, dimension=const.VECTOR_DIMENSION)
    status, ids = milvus_util.insert_vectors(client=client, table_name=table_name, vectors=feats)

    # _, vectors = search_video_or_img(img_path='img/test2/185839.jpg', table_name=table_name)
    # # print(vectors.id_array)
    # print(vectors[0])
    # print(vectors.shape)
