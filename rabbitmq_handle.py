from common.const import *
import json

from feature_extract import *
from rabbitmq_util import *
import threading


# 搜索的回调函数
def handle_search(channel, method, properties, body):
    print(body)
    parameters = json.loads(body)
    table_name = parameters[TABLE_NAME] if TABLE_NAME in parameters else None
    top_k = parameters[TOP_K] if TOP_K in parameters else None
    img_path = parameters[IMG_PATH] if IMG_PATH in parameters else None
    print("开始搜索")
    # 进行搜索
    status, res = search_video_or_img(img_path=img_path, table_name=table_name, top_k=top_k)
    print(res[0]._id_list)
    print(res[0]._dis_list)
    print(status)
    idList = res[0]._id_list
    disList = res[0]._dis_list
    code = status.code
    msg = status.message
    result = dict(code=code, msg=msg, data=dict(milvusIds=idList, disList=disList))
    print(json.dumps(result))
    send_message(SEARCH_QUEUE_RETURN, ROUTING_KEY_SEARCH_RETURN, EXCHANGE_DIRECT, json.dumps(result))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    return json.dumps(result)


# 保存特征数据的回调函数
def handle_save_feats(channel, method, properties, body):
    parameters = json.loads(body)
    print(parameters)
    table_name = parameters[TABLE_NAME] if TABLE_NAME in parameters else None
    print("开始添加数据")
    status, feats_ids = save_feats_to_milvus(keyframe_path=parameters['keyframe_path'],
                                             table_name=table_name)
    code = status.code
    msg = status.message
    picture = parameters["picture"]
    picture = json.loads(picture)
    picture["milvusId"] = feats_ids[0]
    print(picture)
    send_message(SAVE_QUEUE_RETURN, ROUTING_KEY_SAVE_RETURN, EXCHANGE_DIRECT, json.dumps(picture))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    return picture


# 保存视频数据的回调函数
def handle_save_video(channel, method, properties, body):
    parameters = json.loads(body)
    table_name = parameters[TABLE_NAME] if TABLE_NAME in parameters else None
    print("开始插入视频数据")
    video_path = parameters[VIDEO_PATH] if VIDEO_PATH in parameters else None
    video_name = parameters[VIDEO_NAME] if VIDEO_NAME in parameters else None
    status, feats_ids, urls, duration_time, duration = save_video_to_milvus(video_path=video_path,
                                                                            video_name=video_name,
                                                                            table_name=table_name)
    code = status.code
    msg = status.message
    print(feats_ids)
    result = dict(code=code, msg=msg,
                  data=dict(duration=duration, milvusIds=feats_ids, url=urls, duration_time=duration_time))
    send_message(SAVE_VIDEO_QUEUE_RETURN, ROUTING_KEY_SAVE_VIDEO_RETURN, EXCHANGE_DIRECT, json.dumps(result))
    channel.basic_ack(delivery_tag=method.delivery_tag)
    return json.dumps(result)


def handle_Data():
    # 定义监听和处理消息的线程
    search_thread = threading.Thread(target=receive_message,
                                     args=(SEARCH_QUEUE, ROUTING_KEY_SEARCH, EXCHANGE_DIRECT, handle_search))
    save_feats_thread = threading.Thread(target=receive_message,
                                         args=(SAVE_QUEUE_PICTURE, ROUTING_KEY_SAVE_PICTURE, EXCHANGE_DIRECT,
                                               handle_save_feats))
    save_video_thread = threading.Thread(target=receive_message,
                                         args=(SAVE_VIDEO_QUEUE, ROUTING_KEY_SAVE_VIDEO, EXCHANGE_DIRECT,
                                               handle_save_video))
    # test_thread = threading.Thread(target=receive_message, args=("test", "test", "direct", print_mq))
    # test_thread.start()
    search_thread.start()
    save_feats_thread.start()
    save_video_thread.start()


if __name__ == '__main__':
    handle_Data()