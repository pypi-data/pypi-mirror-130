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
    _python_reference = set()
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

        self.init_assert_only_base(reference)
        self.init_assert_ref_len_is_even(reference)

    def _init__chance_to_process_and_override(self, reference) -> set:
        """NanamiLang HashMap, process and override reference"""

        # There we can complete initialization procedure
        # 2. For each next pair of elements (using plain2partitioned)
        #    create _KeyValue instance where key and value 0 and 1 element
        # 1. Set 'reference' as a set of HashMap of created instances

        return set(map(self._KeyValue, shortcuts.plain2partitioned(reference)))

    def get(self, key: Base) -> Base:
        """NanamiLang HashMap, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            key,
            Base,
            message='HashMap.get() key must be derived from Base'
        )

        for e in self.reference():
            if e.key.hashed() == key.hashed():
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
        return '{' + f'{" ".join([f"{i.key.format()} {i.value.format()}" for i in self.elements()])}' + '}'
