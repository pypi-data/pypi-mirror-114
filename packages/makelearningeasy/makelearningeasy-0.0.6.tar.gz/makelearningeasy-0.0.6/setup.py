from setuptools import setup
import os
import sys

if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported.')
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('makelearningeasy/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

download_url = ('https://github.com/MyOpenSource-Projects/makelearningeasy/\
                blob/main/dist/makelearningeasy-0.0.6.whl')

setup(name = 'makelearningeasy',
      packages = ['makelearningeasy'],
      version = '0.0.6',
      description = 'A personal project to improve my learning process',
      author = 'David Foster Wallace',
      author_email = 'davidfosterwallace@gmail.com',
      license = 'Apache2',
      url = 'https://github.com/MyOpenSource-Projects/makelearningeasy',
      install_requires = [ 'selenium', 'opencv-python', 'numpy', 'Pillow'],
      download_url = 'https://github.com/MyOpenSource-Projects/makelearningeasy/archive/0.0.6.tar.gz',
      keywords = ['makelearningeasy', 'easylearning'],
      classifiers = [],
      python_requires='>=3',
      )
