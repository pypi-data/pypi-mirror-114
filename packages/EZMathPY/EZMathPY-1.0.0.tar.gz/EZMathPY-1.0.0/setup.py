from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='EZMathPY',
  version='1.0.0',
  description='a simple python math calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='strikerz',
  author_email='jysonok@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator,math,easy,statistics', 
  packages=find_packages(),
  install_requires=['statistics'] 
)