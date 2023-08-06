import pandas as pd
import numpy as np
from copy import copy


def _preprocessing(x, y):
    if len(x) != len(y):
        print(F'mismatched length of x, y, len(x) == {len(x)} len(y) == {len(y)}')
        return

    x = copy(x)
    y = copy(y)

    factor = pd.Series(x)
    ret = pd.Series(y)

    valid_x = np.isfinite(factor)
    factor = factor[valid_x]
    ret = ret[valid_x]

    factor.dropna(inplace=True)
    ret = ret.reindex(factor.index)

    return factor, ret


def _get_report(indicator, ret):
    """
    :param indicator: pd.Series
    :param ret: pd.Series
    :return: report: pd.DataFrame
    """
    if len(indicator) != len(ret):
        print(F'mismatched length of indicator, pnl, len(indicator) == {len(indicator)} len(ret) == {len(ret)}')
        return

    pnl = indicator * ret

    day_pnl = pnl.resample('D').sum()

    # year PnL
    pnl_y = round(day_pnl.mean() * 251, 2)

    # PoT
    pot = round(pnl.sum() / (indicator.diff().abs().sum()) * 1e4, 2)

    # Sharpe
    sharpe = round(day_pnl.mean() / day_pnl.std() * 16, 2)

    # MDD
    DD_ss = day_pnl.cumsum() - day_pnl.cumsum().expanding(0).max()
    MDD = round(DD_ss.abs().max(), 2)

    def _calc_mddd(m):
        count = 0
        for i in range(-1, -len(m) - 1, -1):
            if m.iloc[i] < 0:
                count += 1
            else:
                break
        return count

    MDDD = int(DD_ss.expanding(0).apply(_calc_mddd).max())

    # WR
    WR = round(day_pnl[day_pnl >= 0].count() / len(day_pnl), 4)

    # Worst
    Worst = day_pnl.min()

    # Skewness
    Skew = day_pnl.skew()

    # Kurtosis
    Kurt = day_pnl.kurtosis()

    Index = ['PnL', 'PoT', 'Sharpe', 'MDD', 'MDDD', 'WR', 'Worst', 'Skewness', 'Kurtosis']
    output = pd.Series([pnl_y, pot, sharpe, MDD, MDDD, WR, Worst, Skew, Kurt], index=Index)

    return output
