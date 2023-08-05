from setuptools import setup, find_packages
__author__ = '神秘的·'
__date__ = '2020/7/17'
with open("README.rst", "r") as L:
    R=L.read()
setup(
    name='ycc', # 名称
    py_modules=['main','__init__','run'],
    version='0.2.4',
    description='三圆计算器,cmd或命令行python -m ycc 或 ycc命令开始运行', # 简单描述
    long_description=R,
    platforms=[
    'Operating System :: MacOS',
    'Operating System :: Windows',
    'Operating System :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',],
    keywords=('ycc'),# 关键字
    author=__author__, # 作者
    author_email='3046479366@qq.com', # 邮箱
    url='http://github.com', # 包含包的项目地址
    license='MIT', # 授权方式
    packages=["p"],
    #package_data = {'p': ['*.py']},
#    package_dir={'p':'y','p':'yh','p':'yz','p':'__main__'},
    #data_files='p/*.py',
    install_requires=['pdsystem'],
    entry_points = {
        'console_scripts': [
            'ycc = run:main',
        ]
    },
    include_package_data=True,
    zip_safe=True,
)