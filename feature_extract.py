import re
from io import BytesIO

import requests as req

from common import vgg_model_init, const
import numpy as np
import milvus_util
import minio_util
from getkeyframes import *
# 初始化VGG模型
from vggnet import VGGNet, vgg_extract_feat
from PIL import Image

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
    #成功后将图片存入minio
    urls = minio_util.put_img_to_miniobatch(const.MINIO_BUCKET_PICTURE, img_list, prefix='keyframe')
    # 将名称从byte转为str，避免json转换出错
    names = [str(name, encoding="utf8") for name in names]
    return feats, names, urls

# 提取特征
def feature_extract_batch(database_path, model):
    img_list = get_imlist(database_path)
    model = model
    print("start extract feature")
    feats, names = model.vgg_extract_feat_batch(database_path)
    total = len(img_list)
    print("extracting feature from %d images in total" % total)
    #成功后将图片存入minio
    urls = minio_util.put_img_to_miniobatch(const.MINIO_BUCKET_PICTURE, img_list, prefix='keyframe')
    print("save keyframe to minio successful! total %d" % len(urls))
    # 将名称从byte转为str，避免json转换出错
    names = [str(name, encoding="utf8") for name in names]
    return feats, names, urls

# 通过图片查询视频或图片
def search_video_or_img(img_path, table_name, top_k=10):
    feats = []
    top_k = int(top_k)
    client = milvus_util.milvus_client()
    tmp_path = get_url_img(url=img_path)
    norm_feat = vgg_extract_feat(img_path=tmp_path, model=model, graph=graph, sess=sess)
    feats.append(norm_feat)
    status, res = milvus_util.search_vectors(client=client, table_name=table_name, vectors=feats, top_k=top_k)
    return status, res


def save_feats_to_milvus(keyframe_path, table_name):
    feats = []
    client = milvus_util.milvus_client()
    tmp_path = get_url_img(url=keyframe_path)
    norm_feat = vgg_extract_feat(img_path=tmp_path, model=model, graph=graph, sess=sess)
    feats.append(norm_feat)
    status, feats_ids = milvus_util.insert_vectors(client=client, table_name=table_name, vectors=feats)
    return status, feats_ids


def save_feats_batch_to_milvus(keyframe_path, table_name):
    client = milvus_util.milvus_client()
    feats, names, urls= feature_extract(database_path=keyframe_path, model=VGGNet())
    status, feats_ids = milvus_util.insert_vectors(client=client, table_name=table_name, vectors=feats)
    return status, feats_ids, names


def save_video_to_milvus(video_path, video_name, table_name=const.MILVUS_KEYFRAME_TABLE):
    client = milvus_util.milvus_client()
    frames_path, duration = extract_frame(file_path=video_path, fps=5, video_name=video_name)
    print(frames_path)
    feats, names, urls = feature_extract_batch(database_path=frames_path, model=VGGNet())
    duration_time = [re.split('[TF.]', time)[len(re.split('[TF.]', time)) - 3] for time in names]
    status, feats_ids = milvus_util.insert_vectors(client=client, table_name=table_name, vectors=feats)
    return status, feats_ids, urls, duration_time, duration


def get_url_img(url, path=const.default_cache_dir):
    response = req.get(url)
    image = Image.open(BytesIO(response.content))
    urll = re.split('[.]',url)
    suffix = urll[len(urll)-1]
    tmp_path = path + "/tmp." + suffix
    image.save(tmp_path)
    return tmp_path


if __name__ == '__main__':
    # feats,names = feature_extract("img/test2", VGGNet())
    # feats = np.array(feats)

    # 初始化一个Milvus类，以后所有的操作都是通过milvus来的
    # milvus = Milvus(host='49.235.115.64',port='19530')

    # print(feats.shape)
    # for feat in feats:
    #     print(feat)

    # 创建连接
    # table_name = 'picture'
    # feats, names = feature_extract("img/test2", VGGNet())
    # client = milvus_util.milvus_client()
    # milvus_util.create_table(client=client, table_name=table_name, dimension=const.VECTOR_DIMENSION)
    # status, ids = milvus_util.insert_vectors(client=client, table_name=table_name, vectors=feats)
    # status, feats_ids, names = save_video_to_milvus("benghuaianime.mp4", 12450, table_name)

    # _, vectors = search_video_or_img(img_path=r"img/test2/184814.jpg", table_name="test1")
    # print(vectors.id_array)
    # print(vectors.distance_array)
    # print(vectors.shape)

    # url = 'http://8.131.87.31:9000/picture/tmp/27e26a934d5b4a1482a0dc6895fb3c7d.png'
    url = 'http://8.131.87.31:9000/picture/tmp/96b18ebd06a1450c83c18ae75f1231bc.jpg'
    path = get_url_img(url=url)
    print(path)
