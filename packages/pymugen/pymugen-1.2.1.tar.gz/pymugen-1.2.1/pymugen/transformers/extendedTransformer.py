# -*- coding: utf-8 -*-

from typing import Union

from pymugen.fasta.sequence import Sequence
from pymugen.transformers.transformer import Transformer
from pymugen.utils.genomics import generate_dict_values

PREFIX_SYMBOLS = ["q", "w", "e", "r"]
MUTATIONS_SYMBOLS = ["a", "s", "d", "f"]
SUFFIX_SYMBOLS = ["z", "x", "c", "v"]


class ExtendedTransformer(Transformer):
    """The extended transformer gets a sequence and transforms it mapping each character
    of the sequence to another depending if the character is in the  prefix, infix or
    suffix.

    Each mapping is defined as:

    - Prefix mapping:
        - A -> q
        - C -> w
        - G -> e
        - T -> r
    - Infix mapping:
        - A -> a
        - C -> s
        - G -> d
        - T -> f
    - Suffix mapping:
        - A -> z
        - C -> x
        - G -> c
        - T -> v

    So, for instance, for a given sequence `Sequence("ACGT", "ACGT", "ACGT")` and a
    mutation `"TGCA"` the  parsers changes it to:

    ```python
        Sequence("qwer", "fdsa", "zxcv", "ACGT")
    ```

    The transformed sequence is named the **extended** sequence.

    Parameters
    ----------
    vcf_path: str
        Path of the vcf file.
    fasta_path: str
        Path of the fasta file.
    """

    prefix_map: dict = generate_dict_values(PREFIX_SYMBOLS)
    """Mapping between nucleotides and the prefix symbols."""

    mutations_map: dict = generate_dict_values(MUTATIONS_SYMBOLS)
    """Mapping between nucleotides and the mutation symbols."""

    suffix_map: dict = generate_dict_values(SUFFIX_SYMBOLS)
    """Mapping between nucleotides and the suffix symbols."""

    name: str = "extended"

    @classmethod
    def method(cls, sequence: Union[tuple, list], mutation: str) -> Sequence:
        """Transforms a sequence into a extended representation.

        Parameters
        ----------
        sequence: tuple
            Sequence.
        mutation: str
            Mutation sequence.

        Returns
        -------
        Transformed sequence.
        """

        left = "".join([cls.prefix_map[nucletid.upper()] for nucletid in sequence[0]])
        middle = "".join([cls.mutations_map[nucletid.upper()] for nucletid in mutation])
        right = "".join([cls.suffix_map[nucletid.upper()] for nucletid in sequence[2]])

        return Sequence(left, middle, right, sequence[1], sequence.chromosome)
