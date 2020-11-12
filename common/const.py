default_cache_dir="./tmp"
input_shape=(224,224,3)

#milvus 常量配置
MILVUS_HOST='8.131.87.31'
MILVUS_PORT='19530'
MILVUS_PICTURE_TABLE = 'picture'
MILVUS_KEYFRAME_TABLE = 'keyframe'
VECTOR_DIMENSION=512

#minio 常量配置
ENDPOINT='8.131.87.31:9000'
ACCESS_KEY='admin'
SECRET_KEY='admin123456'
MINIO_BUCKET_PICTURE = 'picture'