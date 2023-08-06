from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: MacOS :: MacOS X',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: Unix',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
# Setting up

setup(
  name='BlueTE',
  version=VERSION,
  description='A super fast Discord bot project generator',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Spaxly/BlueTE-2.0',
  author='Spaxly',
  license='MIT',
  classifiers=classifiers,
  keywords='discord.py bot generator',
  packages=find_packages(),
  install_requires=['discord.py', 'aiosqlite', 'pipx']
)
