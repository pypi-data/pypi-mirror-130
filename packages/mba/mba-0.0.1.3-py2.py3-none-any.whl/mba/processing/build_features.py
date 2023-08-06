import pandas as pd
from itertools import combinations, groupby
from collections import Counter

from mba.config.core import config




def freq(transactions: pd.Series) -> pd.Series:
    if type(series) == pd.core.series.Series:
        return series.value_counts().rename(config["count"])
    else: 
        return pd.Series(Counter(iterable)).rename(config["count"])


def transaction_count(transactions: pd.Series) -> pd.Series:
    return len(set(series.index))


def get_item_pairs(transactions: pd.Series) -> None:
    """Returns generator that yields item pairs, one at a time"""
    order_item = order_item.reset_index().values
    for order_id, order_object in groupby(order_item, lambda x: x[0]):
        item_list = [item[1] for item in order_object]
        for item_pair in combinations(item_list, 2):
            yield item_pair