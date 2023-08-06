#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/2/1 9:32
@File    : export_strategy_setting.py
@contact : mmmaaaggg@163.com
@desc    : 用于导出 策略设置 生成 json 文件，该文件用于覆盖
.vntrader\cta_strategy_setting.json
.vntrader\portfolio_strategy_setting.json
文件
"""
import json
import logging
import os
import uuid
from collections import OrderedDict
from datetime import date
from typing import List, Union

from ibats_utils.mess import date_2_str

from vnpy_extra.constants import INSTRUMENT_TYPE_SUBSCRIPTION_DIC
from vnpy_extra.db.orm import AccountStrategyMapping, SymbolsInfo, set_account
from vnpy_extra.utils.enhancement import get_instrument_type


def generate_setting_dic(vt_symbols: Union[str, list], strategy_class_name: str,
                         strategy_settings: dict) -> (dict, bool):
    """生成 cta/portfolio setting dict数据"""
    if isinstance(vt_symbols, str):
        vt_symbols = vt_symbols.split('_')

    if len(vt_symbols) == 1:
        is_cta = True
        setting_dic = OrderedDict()
        setting_dic["class_name"] = strategy_class_name
        setting_dic["vt_symbol"] = get_vt_symbols_4_subscription(vt_symbols[0])
        setting_dic["setting"] = settings = OrderedDict()
        settings['class_name'] = strategy_class_name
        for k, v in strategy_settings.items():
            settings[k] = v
    else:
        is_cta = False
        setting_dic = OrderedDict()
        setting_dic["class_name"] = strategy_class_name
        setting_dic["vt_symbols"] = [get_vt_symbols_4_subscription(_) for _ in vt_symbols]
        setting_dic["setting"] = settings = OrderedDict()
        for k, v in strategy_settings.items():
            settings[k] = v

    settings.setdefault('base_position', 1)
    settings.setdefault('stop_opening_pos', 0)
    return setting_dic, is_cta


def get_vt_symbols_4_subscription(vt_symbols):
    """获取可进行行情订阅的合约代码"""
    instrument_type = get_instrument_type(vt_symbols)
    subscription_type = INSTRUMENT_TYPE_SUBSCRIPTION_DIC[instrument_type.upper()]
    return subscription_type + vt_symbols[len(instrument_type):]


def generate_strategy_setting_file(stg_list=None, ignore_stop_opening_pos_stg=False):
    """生成策略配置文件"""
    if stg_list is None:
        stg_list: List[AccountStrategyMapping] = AccountStrategyMapping.get_by_account()

    cta_dic = OrderedDict()
    portfolio_dic = OrderedDict()
    for stats in stg_list:
        if stats.strategy_settings.get('base_position', 1) == 0:
            continue
        symbols = stats.symbols_info.symbols
        strategy_class_name = stats.stg_info.strategy_class_name
        strategy_settings = stats.strategy_settings
        short_name = stats.short_name
        setting_dic, is_cta = generate_setting_dic(symbols, strategy_class_name, strategy_settings)
        if ignore_stop_opening_pos_stg and setting_dic['setting']['stop_opening_pos'] == 1:
            continue
        if is_cta:
            cta_dic[short_name] = setting_dic
        else:
            portfolio_dic[short_name] = setting_dic

    folder_path = os.path.join("output", "strategy_settings", date_2_str(date.today()))
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "cta_strategy_setting.json")
    with open(file_path, 'w') as f:
        json.dump(cta_dic, f, indent=4)

    file_path = os.path.join(folder_path, "portfolio_strategy_setting.json")
    with open(file_path, 'w') as f:
        json.dump(portfolio_dic, f, indent=4)


def replace_vt_symbol_2_main_contract_of_settings(file_path: str):
    """将 settings 中的 vt_symbol 转变为 主力合约"""
    with open(file_path, 'r') as fp:
        settings = json.load(fp)
        for _, setting_dic in settings.items():
            if "vt_symbol" in setting_dic:
                symbols = setting_dic["vt_symbol"]
                symbols_info = SymbolsInfo.get_or_create_curr_symbols(symbols=symbols)
                setting_dic["vt_symbol"] = symbols_info.symbols
            elif "vt_symbols" in setting_dic:
                symbols = setting_dic["vt_symbols"]
                symbols_info = SymbolsInfo.get_or_create_curr_symbols(symbols=symbols)
                setting_dic["vt_symbols"] = symbols_info.symbols
            else:
                logging.warning(f"setting = {setting_dic} 无效")

    with open(file_path, 'w') as fp:
        json.dump(settings, fp, indent=4)


def _test_replace_vt_symbol_2_main_contract_of_settings():
    file_path = r'D:\github\quant_vnpy\scripts\import_export\output\strategy_settings\2021-07-19\cta_strategy_setting_bak.json'
    replace_vt_symbol_2_main_contract_of_settings(file_path=file_path)


def _test_generate_strategy_setting_file():
    # user_name, broker_id = "19510002", "5118"  # 民生期货
    user_name, broker_id = "11859087", "95533"  # 建信期货（资本）
    # user_name, broker_id = "999999", "99999"  # 测试账户
    set_account(user_name, broker_id)
    generate_strategy_setting_file(ignore_stop_opening_pos_stg=True)


if __name__ == "__main__":
    # _test_replace_vt_symbol_2_main_contract_of_settings()
    _test_generate_strategy_setting_file()
