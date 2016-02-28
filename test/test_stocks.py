"""Designed to to be run using PyTest in python 2.7."""
from stock import Stock, Type, Indicator, Trade


def _generate_trades(stock):
    """Generate a sequence of trades to use in test functions.

    :param Stock stock: `Stock` instance to make trades with.
    :return generator: The same `Stock` object is yielded each time a trade is
        made.
    """
    for quantity, indicator, price in (
            (1, Indicator.buy, 5),
            (100, Indicator.buy, 5.67),
            (30, Indicator.sell, 6.12),
            (130, Indicator.buy, 6.88),
            (30, Indicator.sell, 7.9)):
        stock.record_trade(quantity, indicator, price)
        yield


def test_calc_dividend_yield():
    stocks = {
        "TEA": Stock("TEA", Type.common, 0, 100, fixed_dividend=None),
        "POP": Stock("POP", Type.common, 8, 100, fixed_dividend=None),
        "ALE": Stock("ALE", Type.common, 23, 60, fixed_dividend=None),
        "GIN": Stock("GIN", Type.preferred, 8, 100, fixed_dividend=2),
        "JOE": Stock("JOE", Type.common, 13, 250, fixed_dividend=None),
    }
    expected = {
        "TEA": (0, 0, 0, 0, 0),
        "POP": (1.6, 1.4109347442680775, 1.3071895424836601,
                1.1627906976744187, 1.0126582278481011),
        "ALE": (4.6, 4.056437389770723, 3.758169934640523,
                3.3430232558139537, 2.911392405063291),
        "GIN": (40.0, 35.27336860670194, 32.6797385620915,
                29.069767441860467, 25.31645569620253),
        "JOE": (2.6, 2.292768959435626, 2.1241830065359477,
                1.8895348837209303, 1.6455696202531644),
    }
    def verify_calc_dividend_yield():
        for symbol, stock in stocks.iteritems():
            for i, _ in enumerate(_generate_trades(stock)):
                assert stock.calc_dividend_yield() == expected[symbol][i]
    yield verify_calc_dividend_yield


def test_calc_PE_ratio():
    stocks = {
        "TEA": Stock("TEA", Type.common, 0, 100, fixed_dividend=None),
        "POP": Stock("POP", Type.common, 8, 100, fixed_dividend=None),
        "ALE": Stock("ALE", Type.common, 23, 60, fixed_dividend=None),
        "GIN": Stock("GIN", Type.preferred, 8, 100, fixed_dividend=2),
        "JOE": Stock("JOE", Type.common, 13, 250, fixed_dividend=None),
    }
    expected = {
        "TEA": (None, None, None, None, None),
        "POP": (3.125, 4.018612500000001, 4.6818,
                5.916799999999999, 7.801250000000001),
        "ALE": (1.0869565217391306, 1.3977782608695652,
                1.6284521739130435, 2.0580173913043476, 2.7134782608695653),
        "GIN": (0.125, 0.16074449999999998, 0.18727200000000002,
                0.236672, 0.31205),
        "JOE": (1.923076923076923, 2.4729923076923077, 2.881107692307692,
                3.6411076923076924, 4.800769230769231),
    }
    def verify_calc_PE_ratio():
        for symbol, stock in stocks.iteritems():
            for i, _ in enumerate(_generate_trades(stock)):
                assert stock.calc_PE_ratio() == expected[symbol][i]
    yield verify_calc_PE_ratio


def test_record_trade():
    stocks = {
        "GIN": Stock("GIN", Type.preferred, 8, 100, fixed_dividend=2),
        "JOE": Stock("JOE", Type.common, 13, 250, fixed_dividend=None),
    }
    expected = {
        "GIN": [
            [1, Indicator.buy, 5],
            [100, Indicator.buy, 5.67],
            [30, Indicator.sell, 6.12],
            [130, Indicator.buy, 6.88],
            [30, Indicator.sell, 7.9]
        ],
        "JOE": [
            [1, Indicator.buy, 5],
            [100, Indicator.buy, 5.67],
            [30, Indicator.sell, 6.12],
            [130, Indicator.buy, 6.88],
            [30, Indicator.sell, 7.9]
        ],
    }

    def _verify_record_trades():
        # pylint: disable=protected-access
        for symbol, stock in stocks.iteritems():
            for i, _ in enumerate(_generate_trades(stock)):
                all_trades = [[trade.quantity, trade.indicator, trade.price]
                              for trade in stock._trades]
                assert all_trades == expected[symbol][:i + 1]
                # assert timestamps are in order
                timestamps = [trade.timestamp for trade in stock._trades]
                assert timestamps == sorted(timestamps)
    yield _verify_record_trades


def test_calc_VWSP():
    stocks = {
        "GIN": Stock("GIN", Type.preferred, 8, 100, fixed_dividend=2),
    }
    expected = {
        "GIN": [
            5, 5.663366336633663, 5.76793893129771, 6.32183908045977,
            6.484536082474227
        ]
    }

    def _verify_record_trades():
        for symbol, stock in stocks.iteritems():
            for i, _ in enumerate(_generate_trades(stock)):
                assert stock.calc_VWSP() == expected[symbol][i]
    yield _verify_record_trades
