import os
import re
import cv2
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates
from keras.preprocessing import image

phasher = PHash()


def extract_frame(file_path, fps, video_name):
    global duration_time
    count, frame_count = 0, 0
    (path, filename) = os.path.split(file_path)
    print(path)
    save_path = path + "/keyframe"
    cap = cv2.VideoCapture(file_path)
    # 帧数
    frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # 帧率
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    success, image = cap.read()
    print(save_path)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if not os.path.exists(save_path + "/%s" % video_name):
        os.mkdir(save_path + "/%s" % video_name)
    while success:
        # frame_rate:24
        frame_count += 1
        if count % (int(frame_rate / fps)) == 0:
            # cv2.resize(image,())
            cv2.imwrite(save_path + "/%s/%sT%dF%d.jpg" % (video_name, video_name, frame_count / frame_rate, frame_count), image)
            print("wrote a extract_frame: " + save_path + "/%s/%sT%dF%d.jpg" % (
                video_name, video_name, frame_count / frame_rate, frame_count), "duration_time: " + str(int(frame_count / frame_rate)))
        success, image = cap.read()
        count += 1
        # save_status(id, STAGE_EXTRACT, count/allframes)
    cap.release()
    remove_duplicates(str(save_path + "/%s" % video_name))
    duration = []
    duration.append(int(frame/frame_rate))
    return save_path + "/%s" % video_name, duration


# 去除重复的帧文件
def remove_duplicates(file_path):
    # 生成图像目录中所有图像的二值hash编码
    encodings = phasher.encode_images(image_dir=file_path)

    # 对已编码图像寻找重复图像
    duplicates = phasher.find_duplicates(encoding_map=encodings)

    # 删除重复图像
    duplist = list(duplicates.keys())
    for key in duplist:
        print("key :" + key)
        for duplicateImg in duplicates[key]:
            # print("value: " + duplicateImg)
            if os.path.exists(file_path + "/" + duplicateImg):
                print("remove duplicate image : " + duplicateImg)
                os.remove(file_path + "/" + duplicateImg)
                duplicates[key].remove(duplicateImg)
                duplist.remove(duplicateImg)

    print('=' * 20)
    print(duplicates)
    print(type(duplicates))
    print('=' * 20)

    # # 给定一幅图像，显示与其重复的图像
    # plot_duplicates(image_dir=file_path,
    #                 duplicate_map=duplicates,
    #                 filename='prefix411.jpg')


if __name__ == '__main__':
    url = 'http://8.131.87.31:9000/picture/timg67.jpg'
    cap = cv2.VideoCapture(url)
    ret = cap.isOpened()
    while (ret):
        ret, img = cap.read()
        if not ret: break
        cv2.imshow('photo', img)
        cv2.waitKey(0)
    cap.release()

