from minio import *
import common.const as const
import os
import re
minioclient = Minio(endpoint=const.ENDPOINT,
                    access_key=const.ACCESS_KEY,
                    secret_key=const.SECRET_KEY,
                    secure=False)


def put_img_to_minio(bucket_name, file_path, prefix):
    (path,img_name) = os.path.split(file_path)
    path_split = re.split('[/]',path)
    prefix = prefix + '/' + path_split[len(path_split)-1]
    img_name = prefix + '/' + img_name
    minioclient.fput_object(bucket_name=bucket_name, object_name=img_name, file_path=file_path,
                            content_type='image/jpeg')
    url = minioclient.presigned_get_object(bucket_name,img_name)
    url = re.split('[?]', url)[0]
    return url


def put_img_to_miniobatch(bucket_name, file_path_list, prefix):
    count = 0
    urls = []
    for i, img_path in enumerate(file_path_list):
        url = put_img_to_minio(bucket_name,img_path,prefix)
        count += 1
        urls.append(url)
    print("upload keyframe successfully! total %d " % count)
    return urls

if __name__ == '__main__':
    minio_result = put_img_to_minio('picture', 'keyframe/mingrifanzhou/T97F2329.jpg', 'test')
    print(minio_result)
