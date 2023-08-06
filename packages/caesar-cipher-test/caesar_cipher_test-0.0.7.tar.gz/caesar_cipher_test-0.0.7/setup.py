"""
MIT License

Copyright (c) 2021 Berhanu Dagnew
"""
 
from setuptools import setup, find_packages
# long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
# this_directory = Path(__file__).parent
long_description = open('README.md').read()
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='caesar_cipher_test',
  version='0.0.7',
  description='A caesar cipher app and simple python calculator',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='',  # the URL of your package's home page e.g. github link
  author='Berhanu Dagnew',
  author_email='babipanda.learn@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=[''] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)