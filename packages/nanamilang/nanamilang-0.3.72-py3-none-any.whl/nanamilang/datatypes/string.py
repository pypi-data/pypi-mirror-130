"""NanamiLang String Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class String(Base):
    """NanamiLang String Data Type Class"""

    name: str = 'String'
    _expected_type = str
    _python_reference: str
    purpose = 'Encapsulate Python 3 str'

    def __init__(self, reference: str) -> None:
        """Initialize a new String instance"""

        self._hashed = hash(reference)

        super().__init__(reference)

    def format(self, **kwargs) -> str:
        """NanamiLang String, format() method implementation"""

        return f'"{self.reference()}"'
