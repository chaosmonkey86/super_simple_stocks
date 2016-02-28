from stock import Stock, Type, Indicator
import utils

def test_calc_GBCE_all_share_index():
    def _verify_calc_GBCE_all_share_index():
        # generate some fake data
        stock1 = Stock("FOO", Type.common, 1, 80)
        stock1.record_trade(5, Indicator.buy, 9.5)
        stock1.record_trade(50, Indicator.buy, 9.7)

        stock2 = Stock("BAR", Type.preferred, 2, 50, fixed_dividend=3)
        stock2.record_trade(15, Indicator.buy, 10.1)
        stock2.record_trade(30, Indicator.sell, 10.2)

        stock3 = Stock("BAZ", Type.common, 5, 100)
        stock3.record_trade(15, Indicator.buy, 10.1)
        stock3.record_trade(100, Indicator.buy, 9)
        stock3.record_trade(80, Indicator.sell, 15.2)

        result = utils.calc_GBCE_all_share_index([stock1, stock2, stock3])
        expected = 10.460426619142797
        assert result == expected

    yield _verify_calc_GBCE_all_share_index
