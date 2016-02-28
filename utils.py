
def calc_GBCE_all_share_index(stocks):
    """Calculate the GBCE all share index.

    :param list stocks: List of `Stock` objects.
    :return float: Geometric mean of volume weighted stock price for all stocks
        in `stocks`.
    """
    volume_weighted_prices = [stock.calc_VWSP() for stock in stocks]
    product = reduce(lambda x, y: x*y, volume_weighted_prices)
    return product ** (1.0 / len(volume_weighted_prices))

