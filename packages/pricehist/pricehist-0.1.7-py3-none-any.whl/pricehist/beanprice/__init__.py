from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import List, NamedTuple, Optional

from pricehist.series import Series

SourcePrice = NamedTuple(
    "SourcePrice",
    [
        ("price", Decimal),
        ("time", Optional[datetime]),
        ("quote_currency", Optional[str]),
    ],
)


# TODO timezone handling
def source(pricehist_source):
    date_pattern = "%Y-%m-%d"

    class Source:
        def get_latest_price(self, ticker: str) -> Optional[SourcePrice]:
            time_end = datetime.combine(date.today(), datetime.min.time())
            time_begin = time_end - timedelta(days=7)
            prices = self.get_prices_series(ticker, time_begin, time_end)
            if prices:
                return prices[-1]
            else:
                return None

        def get_historical_price(
            self, ticker: str, time: datetime
        ) -> Optional[SourcePrice]:
            prices = self.get_prices_series(ticker, time, time)
            if prices:
                return prices[-1]
            else:
                return None

        def get_prices_series(
            self,
            ticker: str,
            time_begin: datetime,
            time_end: datetime,
        ) -> Optional[List[SourcePrice]]:
            # TODO better parsing, maybe inc type
            base, quote = (ticker + ":").split(":")[0:2]
            type = pricehist_source.types()[0]
            start = time_begin.strftime(date_pattern)
            end = time_end.strftime(date_pattern)
            # TODO exception handling
            series = pricehist_source.fetch(Series(base, quote, type, start, end))
            return [
                SourcePrice(
                    price.amount,
                    datetime.strptime(price.date, date_pattern).replace(
                        tzinfo=timezone.utc
                    ),
                    series.quote,
                )
                for price in series.prices
            ]

    return Source
