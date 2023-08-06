"""NanamiLang IntegerNumber Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class IntegerNumber(Base):
    """NanamiLang IntegerNumber Data Type Class"""

    name: str = 'IntegerNumber'
    _expected_type = int
    _python_reference: int
    purpose = 'Encapsulate Python 3 int'

    def __init__(self, reference: int) -> None:
        """Initialize a new IntegerNumber instance"""

        self._hashed = hash(reference)

        super().__init__(reference)
