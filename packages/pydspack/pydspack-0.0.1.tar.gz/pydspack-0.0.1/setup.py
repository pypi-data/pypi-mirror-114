from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

keywords = ['Data Structure', 'Algorithms', 'pyds']
 
setup(
  name='pydspack',
  version='0.0.1',
  description='A basic library of Data Structures for learning',
  long_description=open('README.txt').read(),
  url='',  
  author='Mandar Parte',
  author_email='mandarparte1709@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=keywords, 
  packages=find_packages(),
  install_requires=[''] 
)