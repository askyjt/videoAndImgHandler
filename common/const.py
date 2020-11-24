default_cache_dir="./tmp"
input_shape=(224,224,3)

#milvus 常量配置
MILVUS_HOST='8.131.87.31'
MILVUS_PORT='19530'
MILVUS_PICTURE_TABLE = 'picture'
MILVUS_KEYFRAME_TABLE = 'keyframe'
VECTOR_DIMENSION=512

#minio 常量配置
# ENDPOINT='8.131.87.31:9000'
# ACCESS_KEY='admin'
# SECRET_KEY='admin123456'

ENDPOINT='127.0.0.1:9000'
ACCESS_KEY='minioadmin'
SECRET_KEY='minioadmin'
MINIO_BUCKET_PICTURE = 'picture'

#RabbitMQ 常量配置
RABBITMQ_HOST='8.131.87.31'
RABBITMQ_PORT='5672'
RABBITMQ_USERNAME='guest'
RABBITMQ_PASSWORD='guest'
VIRTUAL_HOST='/'

#RabbitMQ消息相关常量
EXCHANGE_DIRECT = "direct"

ROUTING_KEY_SAVE_PICTURE = "save.picture"
SAVE_QUEUE_PICTURE = "save_queue_picture"
ROUTING_KEY_SAVE_RETURN = "save.return.picture"
SAVE_QUEUE_RETURN = "save_queue_return_picture"

ROUTING_KEY_SAVE_VIDEO = "save.video"
SAVE_VIDEO_QUEUE = "save_video_queue"
ROUTING_KEY_SAVE_VIDEO_RETURN = "save.video.return"
SAVE_VIDEO_QUEUE_RETURN = "save_video_Queue_return"

ROUTING_KEY_SEARCH = "search"
SEARCH_QUEUE = "search_queue"
ROUTING_KEY_SEARCH_RETURN = "search.return"
SEARCH_QUEUE_RETURN = "search_queue_return"

#请求参数
VIDEO_NAME = 'video_name'
VIDEO_PATH = 'video_path'
IMG_PATH = 'img_path'
TOP_K = 'top_k'
TABLE_NAME = 'table_name'
PARAMETER = 'parameter'