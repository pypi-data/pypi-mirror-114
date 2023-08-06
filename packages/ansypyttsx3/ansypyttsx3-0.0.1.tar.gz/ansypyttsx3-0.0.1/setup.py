from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ansypyttsx3',
  version='0.0.1',
  description='A very easy text to speech',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Anto Joel V',
  author_email='antojoel8020@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='easy text to speech easy pyttsx3', 
  packages=find_packages(),
  install_requires=['pyttsx3'] 
)