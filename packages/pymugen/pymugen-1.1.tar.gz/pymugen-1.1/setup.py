from distutils.core import setup
# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name = 'pymugen',
  packages = ['pymugen'],
  version = '1.1',
  license='MIT',
  description = 'Management about FASTA and VCF files.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alejandro Granados',
  author_email = 'agranadosb55199@outlook.com',
  url = 'https://github.com/agranadosb/pymugen',
  download_url = 'https://github.com/agranadosb/pymugen/archive/refs/heads/main.zip',
  keywords = ['VCF', 'FASTA', 'Genomics'],
  install_requires=[
    'python-levenshtein==0.12.2',
    'pyvcf==0.6.8'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)
