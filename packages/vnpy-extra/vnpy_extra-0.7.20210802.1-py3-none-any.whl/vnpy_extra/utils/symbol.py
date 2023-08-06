"""
@author  : MG
@Time    : 2021/7/21 9:06
@File    : symbol.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from vnpy_extra.constants import SYMBOL_SIZE_DIC
from vnpy_extra.utils.enhancement import get_instrument_type


def get_vt_symbol_multiplier(vt_symbol: str) -> float:
    return SYMBOL_SIZE_DIC[get_instrument_type(vt_symbol)]


def _test_get_vt_symbol_multiplier():
    assert get_vt_symbol_multiplier('rb2101.SHFE') == 10


if __name__ == "__main__":
    _test_get_vt_symbol_multiplier()
