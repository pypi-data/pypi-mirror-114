from setuptools import setup

setup(name='pycftools',
  version='0.1.0',
  description='A simple interface for pycftools api',
  url='https://github.com/Exordio/pycftools',
  author='Ivan Golubev',
  author_email='wecatorz@gmail.com',
  license='MIT',
  py_modules=['pycftools'],
  install_requires=[
    'requests>=2.26.0',
  ],
  zip_safe=False)