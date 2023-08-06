"""NanamiLang Keyword Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Keyword(Base):
    """NanamiLang Keyword Data Type Class"""

    name: str = 'Keyword'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    def __init__(self, reference: str) -> None:
        """Initialize a new Keyword instance"""

        self.init_assert_ref_is_not_empty(reference)

        self._hashed = hash(reference)

        super().__init__(reference)

    def format(self, **kwargs) -> str:
        """NanamiLang Keyword, format() method implementation"""

        return f':{self._python_reference}'
