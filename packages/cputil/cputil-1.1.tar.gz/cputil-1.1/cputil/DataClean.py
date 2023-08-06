import os
import time
import tensorflow as tf
import PIL.Image as Image
from cputil.DataMessage import DataMessage
from cputil.Utils import progress_bar


def __path2code__(path, size):
    """

    :param path: 图片路径
    :param size: 重设大小
    :return: 0
    """
    image = tf.io.read_file(path)  # 读取图片
    if path.split('.')[-1] == 'png':
        try:
            image = tf.image.decode_png(image, channels=3)
        except Exception as exc1:
            print(str(exc1) + '读取png出错：' + path)
            os.remove(path)
            print('已移除：' + path)
            time.sleep(2)
            return 0
    if path.split('.')[-1] == 'jpeg':
        try:
            image = tf.image.decode_jpeg(image, channels=3)
            __jpg_to_png__(path)
            os.remove(path)
        except Exception as exc2:
            print(str(exc2) + '读取jpeg出错：' + path)
            os.remove(path)
            print('已移除：' + path)
            time.sleep(2)
            return 0
    try:
        image = tf.image.resize(image, size)  # 重设为(192, 192)
        image /= 255.0  # 归一化到[0,1]范围
    except Exception as exc3:
        print(str(exc3) + '缩放错误：' + path)
        os.remove(path)
        print('已移除：' + path)
        time.sleep(2)
    return 0


def __jpg_to_png__(path):
    """

    :param path:
    :return:
    """
    image = Image.open(path)
    # 将jpg转换为png
    png_name = path.split('.')[0] + '.png'
    image = image.convert('RGB')
    image.save(png_name)


class DataClean:
    """数据清洗\n
    删除错误数据，将图片格式统一为png\n
    Attributes：
        data_path：数据集路径\n
        image_size：图片重设大小\n
    """
    def __init__(self, data_path, image_size):
        self.data_path = data_path
        self.image_size = image_size
        data_message = DataMessage(data_path)
        count = 1
        try:
            for i in data_message.image_path_data:
                progress_bar(count / data_message.image_count)
                __path2code__(i, image_size)
                count += 1
        except Exception as exc0:
            print(str(exc0) + '\t数据清洗未完成')
            exit(1)
        print('完成数据清洗')
