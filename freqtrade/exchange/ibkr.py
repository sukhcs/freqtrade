"""IBKR exchange subclass"""
"""This file is required by freqtrade, need to exist but does not do much, just overrides
or augments functionality in CCXT-IBKR Exchange class (Check CCXT repo for IBKR class)
"""
import logging
from datetime import datetime

import ccxt

from freqtrade.constants import BuySell
from freqtrade.enums import MarginMode, PriceType, TradingMode
from freqtrade.exceptions import DDosProtection, OperationalException, TemporaryError
from freqtrade.exchange import Exchange
from freqtrade.exchange.common import retrier
from freqtrade.exchange.exchange_types import CcxtOrder, FtHas
from freqtrade.misc import safe_value_fallback2


logger = logging.getLogger(__name__)


class ibkr(Exchange):
    """
    Developed by: Sukhvinder Singh Chauhan 16 Oct 2025
    Ibkr exchange class. Contains adjustments needed for Freqtrade to work
    with this exchange.

    Please note that this exchange is not included in the list of exchanges
    officially supported by the Freqtrade development team. So some features
    may still not work as expected.
    """

    unified_account = True  # TBD: figure out what this is

    _ft_has: FtHas = {
        "order_time_in_force": ["GTC", "IOC"],
        "stoploss_on_exchange": True,
        "stoploss_order_types": {"limit": "market"},
        "stop_price_param": "stopPrice",
        "stop_price_prop": "stopPrice",
        "l2_limit_upper": 1000,       # TBD: don't know what this is-but let's keep it for now
        "marketOrderRequiresPrice": False,
        "trades_has_history": False,  # Endpoint would support this - but ccxt doesn't.
    }

    _ft_has_futures: FtHas = {
        "needs_trading_fees": True,
        "marketOrderRequiresPrice": False,
        "funding_fee_candle_limit": 90,  # TBD: don't know what this is-but will adjust later
        "stop_price_type_field": "price_type",
        "l2_limit_upper": 300,           # TBD: don't know what this is
        "stoploss_blocks_assets": False, # TBD: don't know what this is
        "stop_price_type_value_mapping": {  # TBD: Some fancy stop orders, eh!
            PriceType.LAST: 0,
            PriceType.MARK: 1,
            PriceType.INDEX: 2,
        },
    }
