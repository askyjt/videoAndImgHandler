import common.const as const
import json

from feature_extract import *
from rabbitmq_util import *


def handle_search(channel, method, properties, body):
    parameters = json.loads(body)
    table_name = parameters['parameter']['table_name'] if 'table_name' in parameters['parameter'] else None
    top_k = parameters['parameter']['top_k'] if 'top_k' in parameters['parameter'] else None
    img_path = parameters['parameter']['img_path'] if 'img_path' in parameters['parameter'] else None
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
    channel.basic_ack(delivery_tag=method.delivery_tag)
    return json.dumps(result)



def handle_Data():
    message = receive_message("search_Queue", "search", "direct", handle_search)
    send_message("search_result_queue", "search_result", "direct", message)


if __name__ == '__main__':
    handle_Data()
