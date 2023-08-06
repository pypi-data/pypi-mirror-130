"""NanamiLang NException Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base
from .string import String
from .hashmap import HashMap
from .keyword import Keyword
from .integernumber import IntegerNumber
from nanamilang.shortcuts import ASSERT_IS_INSTANCE_OF


class NException(Base):
    """NanamiLang NException Data Type Class"""

    name: str = 'NException'
    _expected_type = Exception
    _python_reference: HashMap
    purpose = 'Encapsulate Python 3 Exception'

    def __init__(self, reference: Exception) -> None:
        """NanamiLang NException, initialize new instance"""

        super(NException, self).__init__(reference=reference)
        # and then override self._python_reference as we want

        self._python_reference = HashMap(
            ((Keyword('name'), String(reference.__class__.__name__)),
             (Keyword('message'), String(reference.__str__()))),
        )

        self._to_return_for_reference_method_call = IntegerNumber(1)

    def get(self, key: Keyword) -> Base:
        """NanamiLang NException, get() method implementation"""

        # Tricky moment, I would say :D
        ASSERT_IS_INSTANCE_OF(key, Keyword)

        return self._python_reference.get(key)

    def hashed(self) -> int:
        """NanamiLang NException, hashed() method implementation"""

        return self._python_reference.hashed()

    def reference(self) -> IntegerNumber:
        """NanamiLang NException, reference() method implementation"""

        return self._to_return_for_reference_method_call

    def format(self) -> str:
        """NanamiLang NException, format() method implementation"""

        return f'Python 3 Exception has been occurred\n' \
               f'NanamiLang tried to catch it and encapsulate it in\n' \
               f'<nanamilang.datatypes.nexception.NException> class\n' \
               f'Python 3 Exception class name:\n' \
               f'\t{self._python_reference.get(Keyword("name")).format()}\n' \
               f'Message which had been passed to Python 3 Exception:\n' \
               f'\t{self._python_reference.get(Keyword("message")).format()}\n'
