from setuptools import setup, find_packages

"""
pip install --editable .
表示从本地或开发者模式安装项目，
-e, --editable <路径/网址>

521xiaoJIANG
"""

setup(
  name='gethome',
  version='0.1.3',
  py_modules=find_packages('cli1'),
  install_requires=[
    'Click',
  ],
  entry_points={'console_scripts': [
    'gohome=hello:hello',
    'gethome=hello:gethome'
  ]},
)