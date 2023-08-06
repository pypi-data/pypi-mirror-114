from typing import TYPE_CHECKING

from comb_spec_searcher.strategies.rule import AbstractRule
from tilings import GriddedPerm, Tiling

from .tilings import encode_tiling, tiling_to_gui_json

if TYPE_CHECKING:
    from .verification import VerificationTactics


def rule_as_json(
    rule: AbstractRule[Tiling, GriddedPerm], verification_tactics: "VerificationTactics"
) -> dict:
    """Convert rule to json."""
    return {
        "class_module": rule.__class__.__module__,
        "rule_class": rule.__class__.__name__,
        "strategy": rule.strategy.to_jsonable(),
        "children": [
            tiling_to_gui_json(child, verification_tactics) for child in rule.children
        ],
        "formal_step": rule.formal_step,
        "op": rule.get_op_symbol(),
    }


def original_rule_as_json(rule: AbstractRule[Tiling, GriddedPerm]) -> dict:
    """Convert original rule to json."""
    return {
        "class_module": rule.__class__.__module__,
        "rule_class": rule.__class__.__name__,
        "strategy": rule.strategy.to_jsonable(),
        "children": [encode_tiling(child) for child in rule.children],
    }
