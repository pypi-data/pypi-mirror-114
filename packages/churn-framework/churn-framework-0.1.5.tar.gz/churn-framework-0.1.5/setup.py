from setuptools import setup, find_packages
import os

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
  name = 'churn-framework', 
  packages = find_packages(),
  version = '0.1.5',
  license='MIT',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'A3Data',
  author_email = 'gustavo.resende@a3data.com.br',
  url = 'https://github.com/A3Data/churn-framework',
  download_url = 'https://github.com/A3Data/churn-framework/archive/refs/tags/0.1.tar.gz',
  keywords = ['framework', 'churn', 'metric', 'optimizer'],
  install_requires=[
          'tqdm',
          'seaborn',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ]
)