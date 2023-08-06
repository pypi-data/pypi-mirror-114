import itertools
from typing import TYPE_CHECKING, Iterable, List, Tuple, TypeVar

from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.rule import Rule
from flask import Blueprint, request
from permuta.patterns.perm import Perm
from tilings.assumptions import TrackingAssumption
from tilings.exception import InvalidOperationError
from tilings.griddedperm import GriddedPerm
from tilings.strategies import FactorFactory, RowAndColumnPlacementFactory
from tilings.strategies.assumption_insertion import AddAssumptionsStrategy
from tilings.strategies.fusion import FusionStrategy
from tilings.strategies.obstruction_inferral import ObstructionTransitivityFactory
from tilings.strategies.rearrange_assumption import RearrangeAssumptionFactory
from tilings.strategies.requirement_insertion import RequirementInsertionStrategy
from tilings.strategies.requirement_placement import RequirementPlacementStrategy
from tilings.strategies.row_and_col_separation import RowColumnSeparationStrategy
from tilings.strategies.sliding import SlidingFactory, SlidingStrategy
from tilings.strategies.symmetry import (
    TilingAntidiagonal,
    TilingComplement,
    TilingInverse,
    TilingReverse,
    TilingRotate90,
    TilingRotate180,
    TilingRotate270,
)
from tilings.tiling import Tiling
from werkzeug.exceptions import BadRequest

from ..combinatorics import (
    VerificationTactics,
    decode_key,
    original_rule_as_json,
    rule_as_json,
)
from ..utils import TilingDecodeException

if TYPE_CHECKING:
    ItType = TypeVar("ItType")

strategies_blueprint = Blueprint(
    "strategies_blueprint", __name__, url_prefix="/api/strategies"
)


def _any_neg(iterable: Iterable[int]) -> bool:
    return any(z < 0 for z in iterable)


def _get_request_json() -> dict:
    data = request.get_json()
    if data is None or not isinstance(data, dict):
        raise BadRequest()
    return data


def _first_or_bad(iterable: Iterable["ItType"]) -> "ItType":
    for element in iterable:
        return element
    raise BadRequest()


def _get_tiling_input() -> Tuple[Tiling, VerificationTactics]:
    data = _get_request_json()
    if "tiling" not in data or "verify" not in data:
        raise BadRequest()
    tiling_obj = data["tiling"]
    if not isinstance(tiling_obj, str):
        raise BadRequest()
    try:
        tiling: Tiling = decode_key(tiling_obj)
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    return tiling, verification_tactics


@strategies_blueprint.route("/factor", methods=["POST"])
def factor() -> dict:
    """Apply factor strategy to given tiling."""
    interleaving = request.args.get("interleaving", None)
    tiling, verification_tactics = _get_tiling_input()
    try:
        strats = FactorFactory(interleaving=interleaving)(tiling)
    except InvalidOperationError as exc:
        raise BadRequest() from exc
    strat = _first_or_bad(strats)
    rule = strat(tiling)
    return rule_as_json(rule, verification_tactics)


def _get_row_col_placement_input() -> Tuple[
    Tiling, VerificationTactics, int, bool, int
]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        direction: int = data["dir"]
        row: bool = data["row"]
        idx: int = data["idx"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not (
        isinstance(direction, int) and isinstance(row, bool) and isinstance(idx, int)
    ):
        raise BadRequest()
    if direction < 0 or direction > 3:
        raise BadRequest()
    if (
        idx < 0
        or (row and idx >= tiling.dimensions[1])
        or (not row and idx >= tiling.dimensions[0])
    ):
        raise BadRequest()
    return tiling, verification_tactics, direction, row, idx


@strategies_blueprint.route("/rowcolplace", methods=["POST"])
def row_col_placement() -> dict:
    """Apply row column placement strategy to given tiling."""
    tiling, verification_tactics, direction, row, idx = _get_row_col_placement_input()
    for rule in RowAndColumnPlacementFactory(row, not row, dirs=(direction,))(tiling):
        assert isinstance(rule.strategy, RequirementPlacementStrategy)
        if row and rule.strategy.gps[0].pos[0][1] == idx:
            if len(rule.non_empty_children()) == 1:
                rule_json = rule_as_json(
                    rule.to_equivalence_rule(), verification_tactics
                )
                rule_json["original_rule"] = original_rule_as_json(rule)
                return rule_json
            return rule_as_json(rule, verification_tactics)
        if not row and rule.strategy.gps[0].pos[0][0] == idx:
            if len(rule.non_empty_children()) == 1:
                rule_json = rule_as_json(
                    rule.to_equivalence_rule(), verification_tactics
                )
                rule_json["original_rule"] = original_rule_as_json(rule)
                return rule_json
            return rule_as_json(rule, verification_tactics)
    raise BadRequest()


def _get_cell_insertion_input() -> Tuple[Tiling, VerificationTactics, GriddedPerm]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        x: int = data["x"]
        y: int = data["y"]
        patt: str = data["patt"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not (isinstance(x, int) and isinstance(y, int) and isinstance(patt, str)):
        raise BadRequest()
    if not patt.isdecimal():
        raise BadRequest()
    _x, _y = tiling.dimensions
    if x < 0 or x >= _x or y < 0 or y >= _y:
        raise BadRequest()
    n, value_set = len(patt), set(map(int, patt))
    if len(value_set) != n or not all(
        i in value_set for i in (range(n) if 0 in value_set else range(1, n + 1))
    ):
        raise BadRequest()
    return (
        tiling,
        verification_tactics,
        GriddedPerm.single_cell(Perm.to_standard(patt), (x, y)),
    )


@strategies_blueprint.route("/cellinsertion", methods=["POST"])
def cell_insertion() -> dict:
    """Apply cell insertion strategy to given tiling."""
    tiling, verification_tactics, gp = _get_cell_insertion_input()
    try:
        rule = RequirementInsertionStrategy((gp,))(tiling)
    except StrategyDoesNotApply as exc:
        raise BadRequest() from exc
    if all(
        tiling == ne_child
        for ne_child in filter(lambda t: not t.is_empty(), rule.children)
    ):
        raise BadRequest()
    return rule_as_json(rule, verification_tactics)


@strategies_blueprint.route("/rowcolsep", methods=["POST"])
def row_col_separation() -> dict:
    """Apply row/column separation to given tiling."""
    tiling, verification_tactics = _get_tiling_input()
    try:
        rule = RowColumnSeparationStrategy()(tiling)
    except StrategyDoesNotApply as exc:
        raise BadRequest() from exc
    return rule_as_json(rule, verification_tactics)


def _get_requirement_placement_input() -> Tuple[
    Tiling, VerificationTactics, GriddedPerm, int, int
]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        x: int = data["x"]
        y: int = data["y"]
        direction: int = data["dir"]
        idx: int = data["idx"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not (
        isinstance(x, int) and isinstance(y, int) and isinstance(idx, int),
        isinstance(direction, int),
    ):
        raise BadRequest()
    _x, _y = tiling.dimensions
    if _any_neg((idx, x, y, direction)) or x >= _x or y >= _y or direction > 3:
        raise BadRequest()
    cell = (x, y)
    reqs = list(
        filter(
            lambda req: req.is_single_cell() and req.pos[0] == cell,
            itertools.chain(*tiling.requirements),
        )
    )
    if len(reqs) != 1 or idx >= len(reqs[0]):
        raise BadRequest()
    return tiling, verification_tactics, reqs[0], idx, direction


@strategies_blueprint.route("/reqplace", methods=["POST"])
def requirement_placement() -> dict:
    """Apply requirement placement to given tiling."""
    (
        tiling,
        verification_tactics,
        gp,
        idx,
        direction,
    ) = _get_requirement_placement_input()
    try:
        rule = RequirementPlacementStrategy(
            (gp,), (idx,), direction, include_empty=True
        )(tiling)
    except StrategyDoesNotApply as exc:
        raise BadRequest() from exc
    if all(
        tiling == ne_child
        for ne_child in filter(lambda t: not t.is_empty(), rule.children)
    ):
        raise BadRequest()
    if len(rule.non_empty_children()) == 1:
        rule_json = rule_as_json(rule.to_equivalence_rule(), verification_tactics)
        rule_json["original_rule"] = original_rule_as_json(rule)
        return rule_json
    return rule_as_json(rule, verification_tactics)


def _get_add_assumption_input() -> Tuple[
    Tiling, VerificationTactics, List[GriddedPerm]
]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        pos: List[List[int]] = data["pos"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not isinstance(pos, list) or len(pos) == 0:
        raise BadRequest()
    _x, _y = tiling.dimensions
    gps: List[GriddedPerm] = []
    for coord in pos:
        if not isinstance(coord, list) or len(coord) != 2:
            raise BadRequest()
        x, y = coord
        if not (isinstance(x, int) and isinstance(y, int)):
            raise BadRequest()
        if x < 0 or y < 0 or x >= _x or y >= _y:
            raise BadRequest()
        gps.append(GriddedPerm.single_cell((0,), (x, y)))
    return tiling, verification_tactics, gps


@strategies_blueprint.route("/addassumption", methods=["POST"])
def add_assumption() -> dict:
    """Apply add assumption strategy to given tiling."""
    tiling, verification_tactics, gps = _get_add_assumption_input()
    try:
        rule = AddAssumptionsStrategy((TrackingAssumption(gps),))(tiling)
    except StrategyDoesNotApply as exc:
        raise BadRequest() from exc
    if not rule.children or rule.children[0] == tiling:
        raise BadRequest()
    return rule_as_json(rule, verification_tactics)


def _fusion_input() -> Tuple[Tiling, VerificationTactics, int, bool]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        row: bool = data["row"]
        idx: int = data["idx"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not isinstance(idx, int) or not isinstance(row, bool):
        raise BadRequest()
    if (
        idx < 0
        or (row and idx >= tiling.dimensions[1] - 1)
        or (not row and idx >= tiling.dimensions[0] - 1)
    ):
        raise BadRequest()
    return tiling, verification_tactics, idx, row


@strategies_blueprint.route("/fusion", methods=["POST"])
def fusion() -> dict:
    """Apply fusion strategy to given tiling."""
    tiling, verification_tactics, idx, row = _fusion_input()
    arguments = (idx, None, True) if row else (None, idx, True)
    try:
        rule = FusionStrategy(*arguments)(tiling)
    except StrategyDoesNotApply as exc:
        raise BadRequest() from exc
    return rule_as_json(rule, verification_tactics)


@strategies_blueprint.route("/obstrans", methods=["POST"])
def obstruction_transivity() -> dict:
    """Apply obstruction transivity strategy to given tiling."""
    tiling, verification_tactics = _get_tiling_input()
    strat = _first_or_bad(ObstructionTransitivityFactory()(tiling))
    rule = strat(tiling)
    return rule_as_json(rule, verification_tactics)


def _get_sliding_input() -> Tuple[Tiling, VerificationTactics, int, int]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        idx1: int = data["idx1"]
        idx2: int = data["idx2"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not isinstance(idx1, int) or not isinstance(idx2, int):
        raise BadRequest()
    if (
        max(tiling.dimensions) < 2
        or min(tiling.dimensions) != 1
        or min(idx1, idx2) < 0
        or max(idx1, idx2) >= max(tiling.dimensions)
        or idx1 == idx2
    ):
        raise BadRequest()
    return tiling, verification_tactics, idx1, idx2


@strategies_blueprint.route("/sliding", methods=["POST"])
def sliding() -> dict:
    """Apply sliding strategy to given tiling."""
    tiling, verification_tactics, idx1, idx2 = _get_sliding_input()
    cells = max(tiling.dimensions)
    offset_idx_set = {cells - idx1 - 1, cells - idx2 - 1}
    idx_set = {idx1, idx2}
    sym_type_to_idx_set = {0: idx_set, 1: offset_idx_set, 2: offset_idx_set, 3: idx_set}

    for rule in SlidingFactory(True)(tiling):
        assert isinstance(rule.strategy, SlidingStrategy)
        if {rule.strategy.av_12, rule.strategy.av_123} == sym_type_to_idx_set[
            rule.strategy.symmetry_type
        ]:
            return rule_as_json(rule, verification_tactics)
    raise BadRequest()


def _get_symmetry_input() -> Tuple[Tiling, VerificationTactics, int]:
    data = _get_request_json()
    try:
        tiling = decode_key(data["tiling"])
        verification_tactics = VerificationTactics.from_response_dictionary(
            data["verify"]
        )
        sym_type: int = data["symmetry"]
    except (TypeError, KeyError, ValueError, TilingDecodeException) as exc:
        raise BadRequest() from exc
    if not isinstance(sym_type, int) or not 0 < sym_type < 8:
        raise BadRequest()
    return tiling, verification_tactics, sym_type


@strategies_blueprint.route("/symmetry", methods=["POST"])
def symmetry() -> dict:
    """Apply symmetry strategy to given tiling."""
    tiling, verification_tactics, sym_type = _get_symmetry_input()
    symstrat = {
        1: TilingRotate90(),
        2: TilingRotate180(),
        3: TilingRotate270(),
        4: TilingReverse(),
        5: TilingComplement(),
        6: TilingInverse(),
        7: TilingAntidiagonal(),
    }[sym_type]
    rule: Rule = symstrat(tiling)
    if rule.children[0] == tiling:
        raise BadRequest()
    return rule_as_json(rule, verification_tactics)


@strategies_blueprint.route("/rearrangeassumption", methods=["POST"])
def rearrange_assumption():
    """Apply rearrange assumption strategy to given tiling."""
    tiling, verification_tactics = _get_tiling_input()
    for strat in RearrangeAssumptionFactory()(tiling):
        rule = strat(tiling)
        return rule_as_json(rule, verification_tactics)
    raise BadRequest()
