__author__ = 'rochak'

from EdgarRSS import EdgarRSSReader


class InsiderTrades(EdgarRSSReader):
    def __init__(self):
        super(InsiderTrades, self).__init__()

    def get_filings(self):
        # returns the params used and the feed itself
        try:
            recent_insider_tradings = self.get_insider_trades()
            print(recent_insider_tradings)
        except Exception:
            # no entries found
            pass
