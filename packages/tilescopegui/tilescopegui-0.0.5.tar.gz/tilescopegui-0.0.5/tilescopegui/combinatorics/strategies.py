from typing import TYPE_CHECKING, Optional, Tuple

import tilings.strategies as strats
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.rule import VerificationRule
from permuta.patterns.perm import Perm
from tilings import Tiling
from tilings.strategies.experimental_verification import SubclassVerificationStrategy

if TYPE_CHECKING:
    from .verification import VerificationTactics


def _basic_verify(tiling: Tiling) -> Optional[VerificationRule]:
    try:
        return strats.BasicVerificationStrategy()(tiling)
    except StrategyDoesNotApply:
        return None


def _locally_factorable(tiling: Tiling) -> Optional[VerificationRule]:
    try:
        return strats.LocallyFactorableVerificationStrategy()(tiling)
    except StrategyDoesNotApply:
        return None


def _insertion_encodable(tiling: Tiling) -> Optional[VerificationRule]:
    try:
        return strats.InsertionEncodingVerificationStrategy()(tiling)
    except StrategyDoesNotApply:
        return None


def _one_by_one(tiling: Tiling, basis: Tuple[Perm, ...]):
    try:
        return strats.OneByOneVerificationStrategy(basis)(tiling)
    except StrategyDoesNotApply:
        return None


def _subclass(tiling: Tiling, basis: Tuple[Perm, ...]) -> Optional[VerificationRule]:
    try:
        return SubclassVerificationStrategy(basis)(tiling)
    except StrategyDoesNotApply:
        return None


def _short_obstruction(tiling: Tiling):
    try:
        return strats.ShortObstructionVerificationStrategy()(tiling)
    except StrategyDoesNotApply:
        return None


def verify(
    tiling: Tiling, verification_tactics: "VerificationTactics"
) -> Optional[VerificationRule]:
    """Try to verify tiling and return the rule if any."""
    strat = _basic_verify(tiling)
    if strat is None and verification_tactics.insertion_encodable():
        strat = _insertion_encodable(tiling)
    if strat is None and verification_tactics.locally_factorable():
        strat = _locally_factorable(tiling)
    if strat is None and verification_tactics.short_obstruction():
        strat = _short_obstruction(tiling)
    if strat is None and verification_tactics.one_by_one():
        strat = _one_by_one(tiling, verification_tactics.get_basis())
    if strat is None and verification_tactics.subclass():
        strat = _subclass(tiling, verification_tactics.get_basis())
    return strat


def verify_to_json(
    tiling: Tiling, verification_tactics: "VerificationTactics"
) -> Optional[dict]:
    """Try to verify tiling and return the rule as json if any."""
    rule = verify(tiling, verification_tactics)
    if rule:
        return {
            "class_module": rule.__class__.__module__,
            "rule_class": rule.__class__.__name__,
            "strategy": rule.strategy.to_jsonable(),
            "formal_step": rule.formal_step,
        }
    return None
