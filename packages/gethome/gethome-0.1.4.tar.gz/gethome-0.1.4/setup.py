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
  version='0.1.4',
  description='Xiao shen demo',
  long_description=README,
  long_description_content_type='text/markdown',
  py_modules=find_packages('cli1'),
  install_requires=[
    'Click',
  ],
  entry_points={'console_scripts': [
    'gohome=hello:hello',
    'gethome=hello:gethome'
  ]},
)