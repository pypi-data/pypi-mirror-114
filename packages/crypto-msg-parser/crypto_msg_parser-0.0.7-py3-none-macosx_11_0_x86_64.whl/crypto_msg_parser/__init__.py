import json
from typing import Any, Dict, List, Optional

from crypto_msg_parser._lowlevel import ffi, lib


def _str_to_market_type(market_type: str)->int:
    if market_type == 'spot':
        return lib.Spot
    elif market_type == 'linear_future':
        return lib.LinearFuture
    elif market_type == 'inverse_future':
        return lib.InverseFuture
    elif market_type == 'linear_swap':
        return lib.LinearSwap
    elif market_type == 'inverse_swap':
        return lib.InverseSwap
    elif market_type == 'american_option':
        return lib.AmericanOption
    elif market_type == 'european_option':
        return lib.EuropeanOption
    elif market_type == 'quanto_future':
        return lib.QuantoFuture
    elif market_type == 'quanto_swap':
        return lib.QuantoSwap
    elif market_type == 'move':
        return lib.Move
    elif market_type == 'bvol':
        return lib.BVOL
    else:
        raise ValueError(f'Unknown market type: {market_type}')


def parse_trade(
    exchange: str,
    market_type: str,
    msg: str
)-> List[Dict[str, Any]]:
    json_ptr = lib.parse_trade(
        ffi.new("char[]", exchange.encode("utf-8")),
        _str_to_market_type(market_type),
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        # Copy the data to a python string, then parse the JSON
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)

def parse_l2(
    exchange: str,
    market_type: str,
    msg: str,
    timestamp: Optional[int] = None,
)-> List[Dict[str, Any]]:
    json_ptr = lib.parse_l2(
        ffi.new("char[]", exchange.encode("utf-8")),
        _str_to_market_type(market_type),
        ffi.new("char[]", msg.encode("utf-8")),
        0 if timestamp is None else timestamp,
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)

def parse_funding_rate(
    exchange: str,
    market_type: str,
    msg: str
)-> List[Dict[str, Any]]:
    json_ptr = lib.parse_funding_rate(
        ffi.new("char[]", exchange.encode("utf-8")),
        _str_to_market_type(market_type),
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)
