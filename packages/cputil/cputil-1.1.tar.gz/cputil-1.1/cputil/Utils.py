import tensorflow as tf


def progress_bar(progress_data, style='▉', step=10):
    """进度条打印

    :param progress_data: 进度数据
    :param style: 进度条形状
    :param step: 步长(默认为10;建议设置1 or 10)
    :return: None
    """
    print('\r当前进度：{}{:.2f}%'.format(style * int(progress_data * 100 // step), (progress_data * 100)), end='')


def path_to_image(path, size):
    """png图片解码重设大小

    :param path: 图片路径
    :param size: 图片重设大小
    :return: 图片源码
    """
    image = tf.io.read_file(path)  # 读取图片
    image = tf.image.decode_png(image, channels=3)
    image = tf.image.resize(image, size)  # 原始图片大小为(266, 320, 3)，重设为(192, 192)
    image /= 255.0  # 归一化到[0,1]范围
    return image
