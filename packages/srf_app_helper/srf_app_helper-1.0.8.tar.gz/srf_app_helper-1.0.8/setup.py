from setuptools import find_packages, setup

setup(
    name='srf_app_helper',
    version='1.0.8',
    packages=['srf_app_helper'],
    description="为srf项目打造的app收集管理程序",
    author="WangLaoSi", # 作者
    author_email='103745315@qq.com', # 作者邮箱
    url="https://gitee.com/Wang_LaoSi/srf_app_helper", # 项目主页
    download_url='https://gitee.com/Wang_LaoSi/srf_app_helper/repository/archive/master.zip', # 下载地址
    install_requires=['sanic-plugin-toolkit','sanic_rest_framework'] # 依赖
)
