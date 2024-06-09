import functools
import pandas as pd
from .cache import CacheDateFields, ModelCacheKey
from .common import (
    DataCol,
    IndicatorSymbol,
    ModelSymbol,
    TrainedModel,
)
from .indicator import Indicator
from .scope import StaticScope
from dataclasses import asdict
from numpy.typing import NDArray
from typing import Any, Callable, Collection, Iterable, Mapping, Optional


class ModelSource:


    def __init__(
        self,
        name: str,
        indicator_names: Iterable[str],
        input_data_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]],
        predict_fn: Optional[Callable[[Any, pd.DataFrame], NDArray]],
        kwargs: dict[str, Any],
    ):
        self.name = name
        self.indicators = tuple(indicator_names)
        self._input_data_fn = input_data_fn
        self._predict_fn = predict_fn
        self._kwargs = kwargs

    def prepare_input_data(self, df: pd.DataFrame) -> pd.DataFrame:

        if df.empty:
            return df
        if self._input_data_fn is None:
            df_cols = frozenset(df.columns)
            for ind_name in self.indicators:
                if ind_name not in df_cols:
                    raise ValueError(
                        f"Indicator {ind_name!r} not found in DataFrame."
                    )
            return df[[*self.indicators]]
        return self._input_data_fn(df)