
# pymugen

This module allows to manage data about genomic sequences, specificaly getting sequences from a FASTA file.

The module's other functionality is the ability to get sequences with a mutation from a VCF file and transform it to another representation.


## Installation

Install pymugen with python

```bash
  pip3 install pymugen
```

## Usage/Examples

Fasta example

```python
from pymugen.fasta import FastaReader

fasta = FastaReader("fasta.fa")

chromosome = fasta['chr1']
sequence = chromosome.sequence(10, 5, 5)

sequence[1]
>>> A

sequence[:]
>>> CATGCATGCAT

str(sequence)
>>> C-A-T-G-C,A,T-G-C-A-T

chromosome[5: 16]
>>> CATGCATGCAT
```

VCF example

```python
from pymugen.transformers import ExtendedTransformer
from pymugen.fasta import FastaReader

vcf = ExtendedTransformer("vcf.vcf", "fasta.fa")

fasta = FastaReader("fasta.fa")

chromosome = fasta['chr1']
sequence = chromosome.sequence(10, 5, 5)

mutated = vcf.method(sequence, "CGT")

str(mutated)
>>> 'A|w-q-r-e-w,s-d-f,v-c-x-z-v'

mutated[:]
>>> 'wqrewsdfvcxzv'
```
