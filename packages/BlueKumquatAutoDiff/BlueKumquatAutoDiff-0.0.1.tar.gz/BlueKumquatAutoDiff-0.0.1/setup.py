from setuptools import setup
from os import path
from io import open

this_directory = path.abspath(path.dirname(__file__))

def readme():
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()

with open(path.join(this_directory, 'requirements.txt'),
          encoding='utf-8') as f:
    requirements = f.read().splitlines()


setup(
  name = 'BlueKumquatAutoDiff',
  packages = ['BlueKumquatAutoDiff'], 
  version = '0.0.1',
  license='MIT',
  description = 'Package for Automatic Differentiation functions and objects',
  long_description=readme(),
  long_description_content_type='text/markdown',
  author = 'Jailyn Clark, Mason Burlage, Caitlin Lau, Lu Yu',
  author_email = 'caitlinjlau@gmail.com', 
  url = 'https://github.com/cs107-blue-kumquat/cs107-FinalProject.git',
  keywords = ['Auto-diff'],
  install_requires=requirements,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
