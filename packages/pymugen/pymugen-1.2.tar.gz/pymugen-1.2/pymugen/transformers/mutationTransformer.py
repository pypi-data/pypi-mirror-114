from typing import Union

import Levenshtein
from pymugen.fasta.sequence import Sequence
from pymugen.transformers.extendedTransformer import ExtendedTransformer
from pymugen.utils.genomics import generate_dict_values

MUTATIONS_INSERTION_SYMBOLS = ["t", "y", "u", "i"]
MUTATIONS_EARSED_SYMBOLS = ["g", "h", "j", "k"]
MUTATIONS_SUBSITUTION_SYMBOLS = ["a", "s", "d", "f"]

INSERT = "insert"
DELETE = "delete"
REPLACE = "replace"

MUTATION_TYPES = [
    (INSERT, MUTATIONS_INSERTION_SYMBOLS),
    (DELETE, MUTATIONS_EARSED_SYMBOLS),
    (REPLACE, MUTATIONS_SUBSITUTION_SYMBOLS),
]


class MutationTransformer(ExtendedTransformer):
    """The **mutation transformer** is similar to the **extended transformer**, the
    difference is that the result infix has a different symbol depending on how changed
    is the infix reference and the mutation.
    
    In the mutation transformer, each type of modification between the reference
    and the mutation has a different symbol.

    This means that we can get three types of mutations:

    - **Insertion**
    - **Erase**
    - **Substitution**

    So, if we have "A", "C", "G" and "T" symbols for the infix, each symbol has three
    possible mutations:

        A -> ["A_insertion", "A_earsed", "A_substitution"]
        C -> ["C_insertion", "C_earsed", "C_substitution"]
        G -> ["G_insertion", "G_earsed", "G_substitution"]
        T -> ["T_insertion", "T_earsed", "T_substitution"]

    In this case, this method differentiates between prefix symbols and suffix symbols
    (as the extended transformer), so the mappings of each symbol in each position is:

    - **Prefix**
        - A -> q
        - C -> w
        - G -> e
        - T -> r
    - **Infix**
        - **Insertion**
            - A -> t
            - C -> y
            - G -> u
            - T -> i
        - **Erase**
            - A -> g
            - C -> h
            - G -> j
            - T -> k
        - **Substitution**
            - A -> a
            - C -> s
            - G -> d
            - T -> f
    - **Suffix**
        - A -> z
        - C -> x
        - G -> c
        - T -> v
    
    So, for instance, for a given sequence `Sequence("AA", "AC", "CC")` and a
    mutation `"TTGT"` the  parsers changes it to:

    ```python
        Sequence("qq", "iias", "xx", "AC")
    ```

    The transformed sequence is named the **mutation** sequence.

    Parameters
    ----------
    vcf_path: str
        Path of the vcf file.
    fasta_path: str
        Path of the fasta file.
    """

    name: str = "mutation"

    mutations_map: dict = {
        operation: generate_dict_values(symbols)
        for operation, symbols in MUTATION_TYPES
    }

    @classmethod
    def method(cls, sequence: Union[tuple, list], mutation: str) -> Sequence:
        """Transforms a sequence into a extended representation.

        Parameters
        ----------
        sequence : tuple
            Sequence.
        mutation : str
            Mutation sequence.

        Returns
        -------
        Transformed sequence.
        """
        infix = sequence[1]

        operations = Levenshtein.editops(infix, mutation)

        mutation_type_sequence = []
        for operation in operations:
            mutation_type = operation[0]

            reference_sequence = infix
            index = 1
            if mutation_type == INSERT:
                reference_sequence = mutation
                index = 2

            reference_symbol = reference_sequence[operation[index]]

            mutation_type_symbol = cls.mutations_map[mutation_type][reference_symbol]

            mutation_type_sequence.append(mutation_type_symbol)

        left = "".join([cls.prefix_map[nucletid.upper()] for nucletid in sequence[0]])
        right = "".join([cls.suffix_map[nucletid.upper()] for nucletid in sequence[2]])
        mutation_type_sequence = "".join(mutation_type_sequence)

        return Sequence(left, mutation_type_sequence, right, infix, sequence.chromosome)
