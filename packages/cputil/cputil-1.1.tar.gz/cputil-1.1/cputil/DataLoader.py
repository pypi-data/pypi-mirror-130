import numpy as np
from numpy.random import choice
from sklearn.model_selection import train_test_split
from cputil.DataMessage import DataMessage
from cputil.Utils import *


class DataLoader:
    """数据加载器，用于模型训练中数据的加载\n
    获取数据集信息，将路径信息映射为图片源码，通过get_batch方法取得每轮训练数据。\n
    Attributes：
        data_path：数据集路径\n
        image_size：重设图片大小\n
        train_data：训练数据图片（路径）\n
        test_data：测试数据图片（源码）\n
        train_label：训练数据标签\n
        test_label：测试数据标签\n
        num_train_data：训练数据数量\n
        num_test_data：测试数据数量
    """

    def __init__(self, data_path, image_size):
        print('数据集加载')
        self.data_path = data_path
        self.image_size = image_size
        data_message = DataMessage(data_path)
        self.train_data, self.test_data, self.train_label, self.test_label = train_test_split(
            data_message.image_path_data,
            data_message.data_label,
            test_size=0.2,
            stratify=data_message.data_label,
            shuffle=True)
        self.num_train_data, self.num_test_data = self.train_data.shape[0], self.test_data.shape[0]

        # self.test_data = map(path_to_image, self.test_data)
        memory_data = []
        counter = 1
        # TODO 循环加载
        for i in self.test_data:
            progress_bar(counter / self.num_test_data)
            memory_data.append(path_to_image(i, self.image_size))
            counter += 1
        self.test_data = np.array(memory_data)

    def get_batch(self, batch_size):
        """从数据集中随机取出batch_size个元素并返回

        :param batch_size: batch大小
        :return: 数据，标签
        """
        index = np.random.randint(0, self.num_train_data, batch_size)
        data = []
        for i in index:
            path = self.train_data[i]
            data.append(path_to_image(path, self.image_size))
        label = self.train_label[index]
        data = np.array(data)
        return data, label
