"""
@author  : MG
@Time    : 2021/7/21 15:06
@File    : optimization.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
from enum import Enum
from typing import List, Set, Dict

import cvxpy
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns, DiscreteAllocation

from vnpy_extra.db.export_strategy_setting import generate_strategy_setting_file
from vnpy_extra.db.orm import SymbolsInfo, AccountStrategyMapping, StrategyBacktestStats, set_account
from vnpy_extra.portfolio_management.plot import plot_with_base_position, plot_with_weights
from vnpy_extra.utils.symbol import get_vt_symbol_multiplier


class PortfolioOptimizeGoalEnum(Enum):
    max_sharpe = 'max_sharpe'
    min_volatility = 'min_volatility'


class PortfolioOptimization:

    def __init__(self, stats_list: List[StrategyBacktestStats]):
        self.key_stats_dic: Dict[str, StrategyBacktestStats] = {_.get_stats_key_str(): _ for _ in stats_list}
        # 目前仅考虑 CTA 的情况
        self.key_multiplier_dic = {
            key: get_vt_symbol_multiplier(_.symbols_info.symbols)
            for key, _ in self.key_stats_dic.items()}
        self.key_balance_df_dic: Dict[str, pd.DataFrame] = {
            key: _.get_balance_df() for key, _ in self.key_stats_dic.items()}
        self.balance_df = pd.DataFrame({
            key: df['balance']
            for key, df in self.key_balance_df_dic.items()}).dropna()
        self.profit_df = pd.DataFrame({
            key: df['profit']
            for key, df in self.key_balance_df_dic.items()}).dropna()
        self.ef = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.goal = PortfolioOptimizeGoalEnum.max_sharpe

    def fit(self):
        mu = expected_returns.mean_historical_return(self.balance_df)
        sample_cov = risk_models.sample_cov(self.balance_df)

        # Optimize for maximal Sharpe ratio
        self.ef = EfficientFrontier(mu, sample_cov, weight_bounds=(0, 0.3), solver=cvxpy.ECOS)
        raw_weights = getattr(self.ef, self.goal.value)()
        # self.ef.save_weights_to_file("weights.csv")  # saves to file
        # self.ef.portfolio_performance(verbose=True)  #
        weights = self.get_weights()
        print('*' * 20, 'weights', '*' * 20)
        for num, (name, weight) in enumerate(weights.items(), start=1):
            print(f"{num:2d}) {name} --> {weight * 100:.1f}%")

    def get_weights(self) -> Dict[str, float]:
        return self.ef.clean_weights()

    def get_latest_price(self) -> Dict[str, float]:
        symbols: Set[str] = {_.symbols_info.symbols.split('.')[0] for _ in self.key_stats_dic.values()}
        symbol_price_dic = SymbolsInfo.get_symbol_latest_price_dic(symbols)
        return symbol_price_dic

    def get_base_positions(self, capital=1_000_000) -> Dict[str, int]:
        symbol_price_dic = self.get_latest_price()
        # 该价格为×乘数后的价格
        key_price_dic = {
            k: symbol_price_dic[
                   stats.symbols_info.symbols.split('.')[0].upper()
               ] * get_vt_symbol_multiplier(stats.symbols_info.symbols)
            for k, stats in self.key_stats_dic.items()}
        price_s = pd.Series(key_price_dic)
        da = DiscreteAllocation(self.get_weights(), price_s, capital)
        key_base_positions_dic, leftover = da.lp_portfolio()
        print('*' * 20, 'base_positions', capital, '*' * 20)
        for num, (key, base_positions) in enumerate(key_base_positions_dic.items(), start=1):
            print(f"{num:2d}) {key} --> {base_positions}")
        return key_base_positions_dic

    def plot_fitted(self, *, legend=False):

        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 24))
        axes = axes.flatten()
        self.profit_df[[
            k for k, v in self.get_weights().items() if v > 0.0001
        ]].plot(grid=True, ax=axes[0])
        result = pd.DataFrame([self.profit_df[k] * v for k, v in self.get_weights().items()]).sum(axis=0)
        result.plot(grid=True, ax=axes[1])
        plt.show()

    def update_base_positions(self, *, capital=1_000_000, min_positions=0,
                              stop_opening_pos_if_base_position_zero=False):
        from vnpy_extra.db.orm import database
        with database.atomic():
            key_base_positions_dic = self.get_base_positions(capital=capital)
            for key, stats in self.key_stats_dic.items():
                base_positions = key_base_positions_dic.get(key, min_positions)
                stats.set_base_position(
                    base_positions, stop_opening_pos_if_base_position_zero=stop_opening_pos_if_base_position_zero)

    @staticmethod
    def build_by_account(user_name, broker_id):
        stats_list = AccountStrategyMapping.get_stats_by_account(
            user_name, broker_id)
        return PortfolioOptimization(stats_list)


def _test_po():
    user_name, broker_id = "11859087", "95533"
    capital = 500_000
    set_account(user_name, broker_id)
    po = PortfolioOptimization.build_by_account(user_name, broker_id)
    po.goal = PortfolioOptimizeGoalEnum.min_volatility
    po.fit()
    # po.logger.info(pd.DataFrame([po.get_base_positions()]).T)
    plot_with_weights(po.key_stats_dic.values(), po.get_base_positions(capital=capital))
    po.update_base_positions(
        min_positions=0, stop_opening_pos_if_base_position_zero=True,
        capital=capital)
    generate_strategy_setting_file(
        list(po.key_stats_dic.values()), ignore_stop_opening_pos_stg=True)


if __name__ == "__main__":
    _test_po()
