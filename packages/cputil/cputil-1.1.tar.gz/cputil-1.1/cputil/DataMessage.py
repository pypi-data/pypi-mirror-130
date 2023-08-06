import pathlib
import numpy as np


class DataMessage:
    """数据集基本信息\n
    获取图片数据集图片路径列表，标签列表，标签字典，数据量等信息
    Attributes：
        data_path：数据集路径\n
        label_int_dict：标签整形数值对应字典\n
        int_label_dict：整形数值标签对应字典\n
        image_path_data：图片路径列表\n
        data_label：图片标签\n
        image_count：图片数量\n
    """

    def __init__(self, data_path):
        self.data_path = pathlib.Path(data_path)
        self.label_int_dict = self.get_label_dict()
        self.int_label_dict = dict(zip(self.label_int_dict.values(), self.label_int_dict.keys()))
        self.image_path_data, self.data_label = self.get_dataset()
        self.image_count = len(self.image_path_data)
        print("DataMessage加载完成！")

    def get_label_dict(self):
        """获取标签整型对应字典

        :return: 标签整形数值对应字典
        """
        file_name_train = sorted(item.name for item in self.data_path.glob('*') if item.is_dir())
        label_int_dict = dict((name, index) for index, name in enumerate(file_name_train))  # 将标签对应位整形数值
        return label_int_dict

    def get_dataset(self):
        """返回数据集的数据路径列表和标签列表

        :return: 数据列表，标签列表
        """
        all_image_paths = list(self.data_path.glob('*/*'))  # 生成图片路径列表（WindowsPath）
        all_image_paths = [str(path) for path in all_image_paths]  # 将WindowsPath转为str
        all_image_labels = [self.label_int_dict[pathlib.Path(path).parent.name] for path in all_image_paths]
        return np.array(all_image_paths), np.array(all_image_labels)
