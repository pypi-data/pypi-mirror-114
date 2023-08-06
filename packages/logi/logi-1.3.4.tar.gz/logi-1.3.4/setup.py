from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='logi',
      version='1.3.4',
      description='a loging library',
      packages=['logi'],
      license='MPL-2.0 License',
      author = 'hiikion',
      long_description=long_description,
      url='https://github.com/hiikion/logi',
      zip_safe=False)
