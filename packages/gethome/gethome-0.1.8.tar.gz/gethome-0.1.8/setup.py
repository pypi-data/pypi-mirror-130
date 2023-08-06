import os

from setuptools import setup, find_packages

"""
pip install --editable .
表示从本地或开发者模式安装项目，
-e, --editable <路径/网址>

521xiaoJIANG
"""
pwd = os.path.dirname(__file__)
with open(os.path.join(pwd, 'README.md')) as f:
  README = f.read()

setup(
  name='gethome',
  version='0.1.8',
  description='Xiao shen demo',
  long_description=README,
  long_description_content_type='text/markdown',
  py_modules=find_packages('cli1'),  # 找到包的路径
  package_dir={
    '': 'cli1',
  },
  install_requires=[
    'Click',
  ],
  entry_points={'console_scripts': [
    'gohome=hello:hello',  # 对应包里面的文件，文件里面的方法
    'gethome=hello:gethome'
  ]},
)
