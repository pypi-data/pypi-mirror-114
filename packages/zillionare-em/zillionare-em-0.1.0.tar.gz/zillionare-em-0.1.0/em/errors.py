class EMTraderError(Exception):
    pass


class FetchQuotationError(EMTraderError):
    def __init__(self, msg):
        super().__init__(msg)


class FetchPortfolioError(EMTraderError):
    def __init__(self, account):
        self.account = account
        super().__init__("failed to fetch portfolio of account {account}")


class PlaceOrderError(EMTraderError):
    pass
