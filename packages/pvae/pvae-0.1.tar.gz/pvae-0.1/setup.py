from setuptools import setup, find_packages
import os

with open('requirements.txt') as fp:
        install_requires = fp.read()

setup(name='pvae',
      version='0.1',
      description='Pytorch implementation of Poincare Variational Auto-Encoders',
#     long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      url='https://github.com/emilemathieu/pvae',
      author='Jeffrey Cheng',
      author_email='jeff.s.cheng@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
