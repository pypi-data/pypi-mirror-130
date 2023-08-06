"""NanamiLang HashMap Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from typing import Generator

from nanamilang import shortcuts
from .base import Base
from .collection import Collection
from .vector import Vector


class HashMap(Collection):
    """NanamiLang HashMap Data Type Class"""

    name: str = 'HashMap'
    _expected_type = set
    _default = set()
    _python_reference: set
    purpose = 'Implement HashMap of NanamiLang Base data types'

    class _KeyValue:
        """NanamiLang HashMap _KeyValue sub-class"""

        key: Base
        value: Base

        def __init__(self, src: tuple) -> None:
            """NanamiLang HashMap _KeyValue sub-class __init__()"""

            self.key, self.value = src
            # We can do that as we expect there a tuple of key-value

    def _init__assertions_on_non_empty_reference(self,
                                                 reference) -> None:
        """NanamiLang HashMap, needed assertions listed here"""

        self._init_assert_only_base(reference)
        self._init_assert_ref_length_must_be_even(reference)
        # make-hashmap already takes care, but we must ensure anyway

    def _init__chance_to_process_and_override(self,
                                              reference) -> set:
        """NanamiLang HashMap, process and override reference"""

        # Here we can complete initialization procedure
        # 0. Create partitioned structure
        # 1. Create a table of key hash and key value pair
        # 2. And make unique structure using set comprehension

        partitioned = shortcuts.plain2partitioned(reference)
        table = {k.hashed(): (k, v) for k, v in partitioned}
        return {self._KeyValue(kv_p) for _, kv_p in table.items()}

    def get(self, by: Base) -> Base:
        """NanamiLang HashMap, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            by,
            Base,
            message='HashMap.get() "by" must be Base derived'
        )

        for e in self.reference():
            if e.key.hashed() == by.hashed():
                return e.value
        return self._nil
        # Just use for-loops here, no need for fp-like way here :)

    def elements(self) -> Generator:
        """NanamiLang HashMap, elements() method implementation"""

        # Wrap each HashMap element into a NanamiLang Vector data type
        return (Vector((_.key, _.value)) for _ in self._python_reference)

    def format(self, **kwargs) -> str:
        """NanamiLang HashMap, format() method implementation"""

        # There is no sense to iterate over elements when we can return '{}'
        if not self._python_reference:
            return '{}'
        return '{' + f'{" ".join([f"{i.key.format()} {i.value.format()}" for i in self.reference()])}' + '}'
