from typing import List, Tuple

from permuta.patterns.perm import Perm


class VerificationTactics:
    """Verifications to use."""

    INSERTION_ENCODABLE = 0
    LOCALLY_FACTORABLE = 1
    SHORT_OBSTRUCTION = 2
    ONE_BY_ONE = 3
    SUBCLASS = 4

    @staticmethod
    def _remove_basis_dependent(strats: List[int]):
        return list(filter(lambda s: s < VerificationTactics.ONE_BY_ONE, strats))

    @staticmethod
    def _validate_dict(data: dict) -> None:
        if data is None or not isinstance(data, dict):
            raise ValueError()
        if "strats" not in data or "basis" not in data:
            raise ValueError()

    @staticmethod
    def _validate_content(strats: List[int], basis: List[str]) -> None:
        if not isinstance(strats, list) or not isinstance(basis, list):
            raise ValueError()
        if any(not isinstance(s, int) for s in strats) or any(
            not isinstance(p, str) for p in basis
        ):
            raise ValueError()

    @staticmethod
    def _get_content(data: dict) -> Tuple[List[int], List[str]]:
        VerificationTactics._validate_dict(data)
        strats = data["strats"]
        basis = data["basis"]
        return strats, basis

    @staticmethod
    def _validate_and_extract(data: dict) -> Tuple[List[int], List[str]]:
        strats, basis = VerificationTactics._get_content(data)
        VerificationTactics._validate_content(strats, basis)
        if len(basis) == 0:
            strats = VerificationTactics._remove_basis_dependent(strats)
        return strats, basis

    @classmethod
    def from_response_dictionary(cls, data: dict) -> "VerificationTactics":
        """Convert vertification settings to object."""
        return cls(*VerificationTactics._validate_and_extract(data))

    @classmethod
    def from_response_dictionary_for_root(cls, data: dict) -> "VerificationTactics":
        """Convert vertification settings to object for root."""
        strats, basis = VerificationTactics._validate_and_extract(data)
        strats = VerificationTactics._remove_basis_dependent(strats)
        return cls(strats, basis)

    def __init__(self, strats: List[int], basis: List[str]):
        self._strats = set(strats)
        self._basis = tuple(map(Perm.to_standard, basis))

    def insertion_encodable(self) -> bool:
        """Should insertion encodable be applied?"""
        return VerificationTactics.INSERTION_ENCODABLE in self._strats

    def locally_factorable(self) -> bool:
        """Should locally factorable be applied?"""
        return VerificationTactics.LOCALLY_FACTORABLE in self._strats

    def one_by_one(self) -> bool:
        """Should one by one be applied?"""
        return VerificationTactics.ONE_BY_ONE in self._strats

    def subclass(self) -> bool:
        """Should subclass be applied?"""
        return VerificationTactics.SUBCLASS in self._strats

    def short_obstruction(self) -> bool:
        """Should short obstruction be applied?"""
        return VerificationTactics.SHORT_OBSTRUCTION in self._strats

    def get_basis(self) -> Tuple[Perm, ...]:
        """Get root basis."""
        return self._basis
