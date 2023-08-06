from distutils.core import setup

setup(name='cputil',
      version='1.2',
      description='CNN深度学习项目工具包',
      long_description='CNN深度学习项目工具包,'
                       '包括数据清洗，数据加载器以及docker接口测试',
      author='feiyue_chen',
      author_email='1049465452@qq.com',
      py_modules=["cputil.Utils",
                  "cputil.DataMessage",
                  "cputil.DataClean",
                  "cputil.DataLoader",
                  "cputil.DockerApiTest"]
      )
