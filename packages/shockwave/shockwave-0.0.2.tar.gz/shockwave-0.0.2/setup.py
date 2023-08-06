from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 

setup(
  name='shockwave',
  version='0.0.2',
  description='Useful methods for time series analysis',
  long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Gary Ewing',
  author_email='workburner4321@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='time series analysis', 
  #packages=find_packages(), **  '/home/mhughes/sintel_trailer-480p.mp4'
  #packages = 'C:\Users\studl\Desktop\2021_Python Packages\Posted Packages\shockwave\shockwave',
  #packages = r'\Users\studl\Desktop\2021_Python Packages\Posted Packages\shockwave\shockwave\shockwave',
  packages = ['shockwave'],
  install_requires=[''] 
)