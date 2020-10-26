import os
import cv2
from imagededup.methods import PHash
from imagededup.utils import plot_duplicates

phasher = PHash()


def extract_frame(file_path, fps, prefix, id):
    count, frame_count = 0, 0
    cap = cv2.VideoCapture(file_path)
    framerate = cap.get(cv2.CAP_PROP_FPS)
    success, image = cap.read()
    if not os.path.exists(str("img/%s" % id)):
        os.mkdir("img/%s" % id)
    while success:
        if count % (int(framerate / fps)) == 0:
            cv2.imwrite("img/%s/%s%d.jpg" % (id, prefix, frame_count), image)
            print("wrote a extract_frame: " + "img/%s/%s%d.jpg" % (id, prefix, frame_count))
            frame_count += 1
        success, image = cap.read()
        count += 1
        # save_status(id, STAGE_EXTRACT, count/allframes)
    cap.release()
    remove_duplicates(str("img/%s" % id))


#去除重复的帧文件
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
    extract_frame("kexuejia.mp4",10,"prefix","test2")
    remove_duplicates(r"img/test2")
