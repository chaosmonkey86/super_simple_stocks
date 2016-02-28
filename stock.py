from collections import namedtuple
import datetime
from enum import Enum

Type = Enum("Type", "common preferred")
Indicator = Enum("Indicator", "buy sell")
Trade = namedtuple("Trade", "timestamp quantity indicator price")


class Stock(object):
    """Represents a Stock."""
    def __init__(
            self, symbol, type_, last_dividend, par_value,
            fixed_dividend=None):
        self._price = None
        self._trades = []
        self._symbol = symbol
        self._type = type_
        self._last_dividend = float(last_dividend)
        self._par_value = float(par_value)
        if fixed_dividend is not None:
            self._fixed_dividend = float(fixed_dividend)
        else:
            self._fixed_dividend = None

    def calc_dividend_yield(self):
        """Calculate dividend yield.

        Will return None if no trades have been made.

        :return float: Dividend yield.
        """
        if self._price is None:
            return 0
        if self._type is Type.common:
            return self._last_dividend / self._price
        return (self._fixed_dividend * self._par_value) / self._price

    def calc_PE_ratio(self):
        """Calculate price/earnings ratio.

        Will return None if no trades have been made or no dividends have been
        recorded.

        :return float: Price/earnings ratio.
        """
        if self._last_dividend <= 0 or self._price is None:
            return None
        return self._price / self.calc_dividend_yield()

    def calc_VWSP(self, minutes=5):
        """Calculate volume Weighted Stock Price.

        Will return None if no trades have been made.

        :param float minutes: Last n minutes to use to calculate value.
        :return float: Volume Weighted Stock Price.
        """
        window = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        trades = [trade for trade in self._trades if trade.timestamp > window]
        total_value = sum((trade.quantity * trade.price) for trade in trades)
        num_traded = sum(trade.quantity for trade in trades)
        if not num_traded:
            return None
        return total_value / num_traded

    def record_trade(self, quantity, indicator, price):
        """Record a trade of the stock

        :param int quantity: Number of shares.
        :param Enum indicator: `Indicator.buy` or `Indicator.sell`
        :param float price: Stock price.
        """
        self._price = price
        self._trades.append(
            Trade(datetime.datetime.now(), quantity, indicator, price))

    def __repr__(self):
        return (
            "%s(%s, price=%s type=%s last_dividend=%s, par_value=%s, "
            "fixed_dividend=%s)" % (
                self.__class__.__name__, self._symbol, self._price,
                self._type.name, self._last_dividend, self._par_value,
                self._fixed_dividend))
