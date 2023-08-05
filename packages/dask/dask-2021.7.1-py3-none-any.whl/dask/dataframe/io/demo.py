import numpy as np
import pandas as pd

from ...highlevelgraph import HighLevelGraph
from ...layers import DataFrameIOLayer
from ...utils import random_state_data
from ..core import DataFrame, tokenize

__all__ = ["make_timeseries"]


def make_float(n, rstate):
    return rstate.rand(n) * 2 - 1


def make_int(n, rstate, lam=1000):
    return rstate.poisson(lam, size=n)


names = [
    "Alice",
    "Bob",
    "Charlie",
    "Dan",
    "Edith",
    "Frank",
    "George",
    "Hannah",
    "Ingrid",
    "Jerry",
    "Kevin",
    "Laura",
    "Michael",
    "Norbert",
    "Oliver",
    "Patricia",
    "Quinn",
    "Ray",
    "Sarah",
    "Tim",
    "Ursula",
    "Victor",
    "Wendy",
    "Xavier",
    "Yvonne",
    "Zelda",
]


def make_string(n, rstate):
    return rstate.choice(names, size=n)


def make_categorical(n, rstate):
    return pd.Categorical.from_codes(rstate.randint(0, len(names), size=n), names)


make = {
    float: make_float,
    int: make_int,
    str: make_string,
    object: make_string,
    "category": make_categorical,
}


class MakeTimeseriesPart:
    """
    Wrapper Class for ``make_timeseries_part``
    Makes a timeseries partition.
    """

    def __init__(self, dtypes, freq, kwargs, columns=None):
        self.columns = columns or list(dtypes.keys())
        self.dtypes = {c: dtypes[c] for c in self.columns}
        self.freq = freq
        self.kwargs = kwargs

    def project_columns(self, columns):
        """Return a new MakeTimeseriesPart object with
        a sub-column projection.
        """
        if columns == self.columns:
            return self
        return MakeTimeseriesPart(
            self.dtypes,
            self.freq,
            self.kwargs,
            columns=columns,
        )

    def __call__(self, part):
        divisions, state_data = part
        if isinstance(state_data, int):
            state_data = random_state_data(1, state_data)
        return make_timeseries_part(
            divisions[0], divisions[1], self.dtypes, self.freq, state_data, self.kwargs
        )


def make_timeseries_part(start, end, dtypes, freq, state_data, kwargs):
    index = pd.date_range(start=start, end=end, freq=freq, name="timestamp")
    state = np.random.RandomState(state_data)
    columns = {}
    for k, dt in dtypes.items():
        kws = {
            kk.rsplit("_", 1)[1]: v
            for kk, v in kwargs.items()
            if kk.rsplit("_", 1)[0] == k
        }
        columns[k] = make[dt](len(index), state, **kws)
    df = pd.DataFrame(columns, index=index, columns=sorted(columns))
    if df.index[-1] == end:
        df = df.iloc[:-1]
    return df


def make_timeseries(
    start="2000-01-01",
    end="2000-12-31",
    dtypes={"name": str, "id": int, "x": float, "y": float},
    freq="10s",
    partition_freq="1M",
    seed=None,
    **kwargs
):
    """Create timeseries dataframe with random data

    Parameters
    ----------
    start: datetime (or datetime-like string)
        Start of time series
    end: datetime (or datetime-like string)
        End of time series
    dtypes: dict
        Mapping of column names to types.
        Valid types include {float, int, str, 'category'}
    freq: string
        String like '2s' or '1H' or '12W' for the time series frequency
    partition_freq: string
        String like '1M' or '2Y' to divide the dataframe into partitions
    seed: int (optional)
        Randomstate seed
    kwargs:
        Keywords to pass down to individual column creation functions.
        Keywords should be prefixed by the column name and then an underscore.

    Examples
    --------
    >>> import dask.dataframe as dd
    >>> df = dd.demo.make_timeseries('2000', '2010',
    ...                              {'value': float, 'name': str, 'id': int},
    ...                              freq='2H', partition_freq='1D', seed=1)
    >>> df.head()  # doctest: +SKIP
                           id      name     value
    2000-01-01 00:00:00   969     Jerry -0.309014
    2000-01-01 02:00:00  1010       Ray -0.760675
    2000-01-01 04:00:00  1016  Patricia -0.063261
    2000-01-01 06:00:00   960   Charlie  0.788245
    2000-01-01 08:00:00  1031     Kevin  0.466002
    """
    divisions = list(pd.date_range(start=start, end=end, freq=partition_freq))
    npartitions = len(divisions) - 1
    if seed is None:
        # Get random integer seed for each partition. We can
        # call `random_state_data` in `MakeTimeseriesPart`
        state_data = np.random.randint(2e9, size=npartitions)
    else:
        state_data = random_state_data(npartitions, seed)
    label = "make-timeseries-"
    name = label + tokenize(start, end, dtypes, freq, partition_freq, state_data)

    # Build parts
    parts = []
    for i in range(len(divisions) - 1):
        parts.append((divisions[i : i + 2], state_data[i]))

    # Construct Layer and Collection
    layer = DataFrameIOLayer(
        name=name,
        columns=None,
        inputs=parts,
        io_func=MakeTimeseriesPart(dtypes, freq, kwargs),
        label=label,
    )
    graph = HighLevelGraph({name: layer}, {name: set()})
    head = make_timeseries_part("2000", "2000", dtypes, "1H", state_data[0], kwargs)
    return DataFrame(graph, name, head, divisions)


class GenerateDay:
    """
    Wrapper Class for ``generate_day``
    Generates daily-stock data for a day.
    """

    def __init__(self, freq):
        self.freq = freq

    def __call__(self, part):
        s, seed = part
        if isinstance(seed, int):
            seed = random_state_data(1, seed)
        return generate_day(
            s.name,
            s.loc["Open"],
            s.loc["High"],
            s.loc["Low"],
            s.loc["Close"],
            s.loc["Volume"],
            freq=self.freq,
            random_state=seed,
        )


def generate_day(
    date,
    open,
    high,
    low,
    close,
    volume,
    freq=pd.Timedelta(seconds=60),
    random_state=None,
):
    """Generate a day of financial data from open/close high/low values"""
    if not isinstance(random_state, np.random.RandomState):
        random_state = np.random.RandomState(random_state)
    if not isinstance(date, pd.Timestamp):
        date = pd.Timestamp(date)
    if not isinstance(freq, pd.Timedelta):
        freq = pd.Timedelta(freq)

    time = pd.date_range(
        date + pd.Timedelta(hours=9),
        date + pd.Timedelta(hours=12 + 4),
        freq=freq / 5,
        name="timestamp",
    )
    n = len(time)
    while True:
        values = (random_state.random_sample(n) - 0.5).cumsum()
        values *= (high - low) / (values.max() - values.min())  # scale
        values += np.linspace(
            open - values[0], close - values[-1], len(values)
        )  # endpoints
        assert np.allclose(open, values[0])
        assert np.allclose(close, values[-1])

        mx = max(close, open)
        mn = min(close, open)
        ind = values > mx
        values[ind] = (values[ind] - mx) * (high - mx) / (values.max() - mx) + mx
        ind = values < mn
        values[ind] = (values[ind] - mn) * (low - mn) / (values.min() - mn) + mn
        # The process fails if min/max are the same as open close.  This is rare
        if np.allclose(values.max(), high) and np.allclose(values.min(), low):
            break

    s = pd.Series(values.round(3), index=time)
    rs = s.resample(freq)
    # TODO: add in volume
    return pd.DataFrame(
        {"open": rs.first(), "close": rs.last(), "high": rs.max(), "low": rs.min()}
    )


def daily_stock(
    symbol,
    start,
    stop,
    freq=pd.Timedelta(seconds=1),
    data_source="yahoo",
    random_state=None,
):
    """Create artificial stock data

    This data matches daily open/high/low/close values from Yahoo! Finance, but
    interpolates values within each day with random values.  This makes the
    results look natural without requiring the downloading of large volumes of
    data.  This is useful for education and benchmarking.

    Parameters
    ----------
    symbol: string
        A stock symbol like "GOOG" or "F"
    start: date, str, or pd.Timestamp
        The start date, input will be fed into pd.Timestamp for normalization
    stop: date, str, or pd.Timestamp
        The start date, input will be fed into pd.Timestamp for normalization
    freq: timedelta, str, or pd.Timedelta
        The frequency of sampling
    data_source: str, optional
        defaults to 'yahoo'.  See pandas_datareader.data.DataReader for options
    random_state: int, np.random.RandomState object
        random seed, defaults to randomly chosen

    Examples
    --------
    >>> import dask.dataframe as dd  # doctest: +SKIP
    >>> df = dd.demo.daily_stock('GOOG', '2010', '2011', freq='1s')  # doctest: +SKIP
    >>> df  # doctest: +SKIP
    Dask DataFrame Structure:
                           close     high      low     open
    npartitions=252
    2010-01-04 09:00:00  float64  float64  float64  float64
    2010-01-05 09:00:00      ...      ...      ...      ...
    ...                      ...      ...      ...      ...
    2010-12-31 09:00:00      ...      ...      ...      ...
    2010-12-31 16:00:00      ...      ...      ...      ...
    Dask Name: from-delayed, 504 tasks

    >>> df.head()  # doctest: +SKIP
                           close     high      low     open
    timestamp
    2010-01-04 09:00:00  626.944  626.964  626.944  626.951
    2010-01-04 09:00:01  626.906  626.931  626.906  626.931
    2010-01-04 09:00:02  626.901  626.911  626.901  626.905
    2010-01-04 09:00:03  626.920  626.920  626.905  626.905
    2010-01-04 09:00:04  626.894  626.917  626.894  626.906
    """
    from pandas_datareader import data

    df = data.DataReader(symbol, data_source, start, stop)
    npartitions = len(df)
    if random_state is None:
        # Get random integer seed for each partition. We can
        # call `random_state_data` in `GenerateDay`
        seeds = np.random.randint(2e9, size=npartitions)
    else:
        seeds = random_state_data(npartitions, random_state=random_state)

    label = "daily-stock-"
    name = label + tokenize(symbol, start, stop, freq, data_source, seeds)

    divisions = []
    inputs = []
    for i, seed in zip(range(npartitions), seeds):
        s = df.iloc[i]
        if s.isnull().any():
            continue
        inputs.append((s, seed))
        divisions.append(s.name + pd.Timedelta(hours=9))

    layer = DataFrameIOLayer(
        name=name,
        columns=None,
        inputs=inputs,
        io_func=GenerateDay(freq),
        label=label,
    )

    graph = HighLevelGraph({name: layer}, {name: set()})
    meta = generate_day("2000-01-01", 1, 2, 0, 1, 100)
    return DataFrame(graph, name, meta, divisions)
