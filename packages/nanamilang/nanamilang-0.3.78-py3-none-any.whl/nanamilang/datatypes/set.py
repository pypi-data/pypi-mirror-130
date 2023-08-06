"""NanamiLang Set Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)

from nanamilang import shortcuts
from .base import Base
from .collection import Collection


class Set(Collection):
    """NanamiLang Set Data Type Class"""

    name: str = 'Set'
    _expected_type = set
    _default = set()
    _python_reference: set
    purpose = 'Implements Set of NanamiLang Base data types'

    def _init__chance_to_process_and_override(self,
                                              reference) -> set:
        """NanamiLang Set, process and override reference"""

        # Here we can complete initialization procedure
        # 1. Create a table of element hash and element itself
        # 2. And make unique structure using set comprehension

        tbl = {elem.hashed(): elem for elem in reference}
        return {tbl.get(hashed) for hashed in set(tbl.keys())}

    def get(self, by: Base) -> Base:
        """NanamiLang Set, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            by,
            Base,
            message='Set.get() "by" must be Base derived'
        )

        for e in self.reference():
            if e.hashed() == by.hashed():
                return e
        return self._nil
        # Just use for-loops here, no need for fp-like way here :)

    def format(self, **kwargs) -> str:
        """NanamiLang Set, format() method implementation"""

        # There is no sense to iterate over elements when we can return '#{}'
        if not self._python_reference:
            return '#{}'
        return '#{' + f'{" ".join((i.format() for i in self.reference()))}' + '}'
