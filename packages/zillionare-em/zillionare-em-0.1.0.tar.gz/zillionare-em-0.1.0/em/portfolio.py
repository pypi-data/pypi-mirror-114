class Portfolio:
    mapping = {
        "Kqzj": "withdrawable",
        "Kyzj": "avail",
        "Zjye": "cash",
        "Zxsz": "market_value",
        "Zzc": "assets",
        "Ljyk": "profit",
    }

    def __init__(
        self,
        assets=0.0,
        market_value=0.0,
        cash=0.0,
        avail=0.0,
        withdrawable=0.0,
        profit=0.0,
    ):
        # 总资产
        self.assets = assets
        # 总市值
        self.market_value = market_value
        # 现金，资金余额
        self.cash = cash
        # 可用资金（即可用以买入股票的资金）
        self.avail = avail
        # 可取资金
        self.withdrawable = withdrawable
        # 持仓盈亏
        self.profit = profit

        # 持仓
        self.positions = []

    @classmethod
    def convert(cls, data: dict) -> dict:
        return {v: float(data[k]) for k, v in cls.mapping.items()}

    def as_dict(self):
        return {
            "assets": self.assets,
            "market_value": self.market_value,
            "cash": self.cash,
            "avail": self.avail,
            "withdrawable": self.withdrawable,
            "profit": self.profit,
            "positions": self.positions,
        }
