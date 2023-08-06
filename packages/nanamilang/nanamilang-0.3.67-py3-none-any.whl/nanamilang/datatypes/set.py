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
    _python_reference: set = set()
    purpose = 'Implements Set of NanamiLang Base data types'

    def get(self, element: Base) -> Base:
        """NanamiLang Set, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            element,
            Base,
            message='Set.get() element must be derived from Base'
        )

        for e in self.reference():
            if e.hashed() == element.hashed():
                return e
        return self._nil
        # Just use for-loops here, no need for fp-like way here :)

    def format(self, **kwargs) -> str:
        """NanamiLang Set, format() method implementation"""

        # There is no sense to iterate over elements when we can return '#{}'
        if not self._python_reference:
            return '#{}'
        return '#{' + f'{" ".join((i.format() for i in self.elements()))}' + '}'
