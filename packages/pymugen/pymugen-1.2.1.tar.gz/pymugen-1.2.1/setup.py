from setuptools import find_packages, setup

setup(
  name = 'pymugen',
  packages = find_packages(),
  version = '1.2.1',
  license='MIT',
  description = 'Management about FASTA and VCF files.',
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
  long_description="""
  pymugen
  -------

  This module allows to manage data about genomic sequences, specificaly getting sequences from a FASTA file.

  The module's other functionality is the ability to get sequences with a mutation from a VCF file and transform it to another representation.


  Installation
  ------------

  Install pymugen with python

  ``pip3 install pymugen``

  Usage/Examples
  --------------

  Fasta example

  ::

    from pymugen.fasta import FastaReader

    fasta = FastaReader("fasta.fa")

    chromosome = fasta['chr1']
    sequence = chromosome.sequence(10, 5, 5)

    sequence[1]
    # A

    sequence[:]
    # CATGCATGCAT

    str(sequence)
    # C-A-T-G-C,A,T-G-C-A-T

    chromosome[5: 16]
    # CATGCATGCAT


  VCF example

  ::

    from pymugen.transformers import ExtendedTransformer
    from pymugen.fasta import FastaReader

    vcf = ExtendedTransformer("vcf.vcf", "fasta.fa")

    fasta = FastaReader("fasta.fa")

    chromosome = fasta['chr1']
    sequence = chromosome.sequence(10, 5, 5)

    mutated = vcf.method(sequence, "CGT")

    str(mutated)
    # 'A|w-q-r-e-w,s-d-f,v-c-x-z-v'

    mutated[:]
    # 'wqrewsdfvcxzv'

  """,
)
