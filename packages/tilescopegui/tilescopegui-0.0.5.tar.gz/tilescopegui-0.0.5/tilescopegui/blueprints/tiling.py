from typing import List, Optional, Tuple, Union

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from tilings.tiling import Tiling
from werkzeug.exceptions import BadRequest

from ..combinatorics import VerificationTactics, decode_keys, tiling_to_gui_json
from ..utils import TilingDecodeException

tiling_blueprint = Blueprint("tiling_blueprint", __name__, url_prefix="/api/tiling")


def _get_tiling_from_basis_input() -> Tuple[Union[str, dict], VerificationTactics]:
    data: Optional[dict] = request.get_json()
    if data is None or not isinstance(data, dict):
        raise BadRequest()
    if "tiling" not in data or "verify" not in data:
        raise BadRequest()
    tiling_resp = data["tiling"]
    if not isinstance(tiling_resp, (str, dict)):
        raise BadRequest
    try:
        verification_tactics = VerificationTactics.from_response_dictionary_for_root(
            data["verify"]
        )
    except ValueError as exc:
        raise BadRequest() from exc
    return tiling_resp, verification_tactics


@tiling_blueprint.route("/init", methods=["POST"])
def tiling_from_basis() -> dict:
    """Get root tiling."""
    tiling_resp, verification_tactics = _get_tiling_from_basis_input()
    try:
        if isinstance(tiling_resp, str):
            tiling: Tiling = Tiling.from_string(tiling_resp)
        else:
            tiling = Tiling.from_dict(tiling_resp)
    except (TypeError, KeyError, ValueError) as exc:
        raise BadRequest() from exc
    return tiling_to_gui_json(tiling, verification_tactics)


@tiling_blueprint.route("/decode", methods=["POST"])
def tilings_from_keys() -> Response:
    """Given a list of encodes keys, convert to tilings."""
    data: Optional[List[str]] = request.get_json()
    if data is None or not isinstance(data, list):
        raise BadRequest()
    try:
        return jsonify([tiling.to_jsonable() for tiling in decode_keys(data)])
    except (TilingDecodeException, TypeError, KeyError, ValueError) as exc:
        raise BadRequest() from exc


@tiling_blueprint.route("/repl", methods=["POST"])
def tiling_repl() -> Response:
    """Given an encoded key, convert to repl"""
    data: Optional[str] = request.get_json()
    if data is None or not isinstance(data, str):
        raise BadRequest()
    try:
        tiling: Tiling = next(decode_keys([data]))
        return jsonify(repr(tiling))
    except (
        StopIteration,
        TilingDecodeException,
        TypeError,
        KeyError,
        ValueError,
    ) as exc:
        raise BadRequest() from exc
