from typing import List, Optional, Union

from flask import Blueprint, request
from tilings.tiling import Tiling
from werkzeug.exceptions import BadRequest

from ..combinatorics import decode_keys, tiling_to_gui_json
from ..utils import TilingDecodeException

tiling_blueprint = Blueprint("tiling_blueprint", __name__, url_prefix="/api/tiling")


@tiling_blueprint.route("/init", methods=["POST"])
def tiling_from_basis() -> dict:
    """Get a root tiling."""
    data: Optional[Union[dict, str]] = request.get_json()
    if data is None:
        raise BadRequest()
    try:
        if isinstance(data, str):
            tiling: Tiling = Tiling.from_string(data)
        else:
            tiling = Tiling.from_dict(data)
    except (TypeError, KeyError, ValueError) as exc:
        raise BadRequest() from exc
    return tiling_to_gui_json(tiling)


@tiling_blueprint.route("/decode", methods=["POST"])
def tilings_from_keys() -> List[Tiling]:
    """Given a list of encodes keys, convert to tilings."""
    data: Optional[List[str]] = request.get_json()
    if data is None or not isinstance(data, list):
        raise BadRequest()
    try:
        return list(decode_keys(data))
    except TilingDecodeException as exc:
        raise BadRequest() from exc
