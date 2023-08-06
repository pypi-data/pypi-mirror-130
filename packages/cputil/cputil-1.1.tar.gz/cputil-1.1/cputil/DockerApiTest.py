import json
import numpy as np
import requests


class DockerApiTest:
    """Docker接口测试\n
    Attributes：
        docker_api：docker接口\n
    """

    def __init__(self, docker_api, test_data):
        self.docker_api = docker_api

    def test(self, test_data):
        """
        :param test_data: 测试数据，应为测试图片列表\n
        :return: 预测结果
        """
        data = json.dumps({
            "instances": test_data.tolist()
        })
        headers = {"content-type": "application/json"}
        json_response = requests.post(self.docker_api, data=data, headers=headers)
        predictions = np.array(json.loads(json_response.text)['predictions'])
        result = np.argmax(predictions, axis=-1)
        return result
