from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='demofirstpackage',
  version='0.0.1',
  description='A very basic demo',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mandar Parte',
  author_email='mandarparte1709@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='demo', 
  packages=find_packages(),
  install_requires=[''] 
)