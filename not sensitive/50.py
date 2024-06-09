   def __init__(self):
        self.logger = Logger(self)
        self.data_source_cache: Optional[Cache] = None
        self.data_source_cache_ns: str = ""
        self.indicator_cache: Optional[Cache] = None
        self.indicator_cache_ns: str = ""
        self.model_cache: Optional[Cache] = None
        self.model_cache_ns: str = ""
        self._indicators = {}
        self._model_sources = {}
        self.default_data_cols = frozenset(
            (
                DataCol.DATE.value,
                DataCol.OPEN.value,
                DataCol.HIGH.value,
                DataCol.LOW.value,
                DataCol.CLOSE.value,
                DataCol.VOLUME.value,
                DataCol.VWAP.value,
            )
        )
        self.custom_data_cols = set()
        self._cols_frozen: bool = False

    def set_indicator(self, indicator):

        self._indicators[indicator.name] = indicator

    def has_indicator(self, name: str) -> bool:

     
        return name in self._indicators

    def get_indicator(self, name: str):

        if not self.has_indicator(name):
            raise ValueError(f"Indicator {name!r} does not exist.")
        return self._indicators[name]