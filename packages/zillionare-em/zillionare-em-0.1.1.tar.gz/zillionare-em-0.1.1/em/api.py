"""Main module."""
import asyncio
import datetime
import json
import logging
import os
import random
from typing import Any, Union

import arrow
import pyppeteer as pp
from pyppeteer.browser import Browser
from pyppeteer.page import Page
from sanic import request, response

from em.basecrawler import BaseCrawler
from em.errors import FetchPortfolioError, FetchQuotationError, PlaceOrderError
from em.portfolio import Portfolio
from em.quotation import Quotation
from em.selectors import Selectors
from em.util import datetime_as_filename

logger = logging.getLogger(__name__)


class EMTraderWebInterface(BaseCrawler):
    def __init__(self, model, screenshot_dir=None):
        if screenshot_dir is None:
            screenshot_dir = os.path.expanduser("~/em/screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

        super().__init__("https://jy.xzsec.com", screenshot_dir)
        self._browser: Browser = None
        self._decay_retry = 1
        self._model = model
        self._is_authed = False
        self._portfolio = None

        self.account = os.getenv("ACCOUNT")

    @property
    def is_authed(self):
        return self._is_authed

    @property
    def portfolio(self):
        return self._portfolio

    async def init(self, *args):
        await self.start()
        await self.login()
        await self._get_portfolio()

    async def stop(self, *args):
        await super().stop()

    async def _dismiss_notice(self, page: Page):
        notice = await page.xpath(Selectors.notice_btn)
        if notice:
            await notice[0].click()

    async def login(self):
        try:
            page, _ = await self.goto(self._base_url)

            await self._dismiss_notice(page)

            img_src = await page.Jeval(Selectors.captcha_img_src, "node => node.src")
            code = await self._hack_captcha(img_src)

            password = os.environ["PASSWORD"]

            await page.Jeval(Selectors.account, f"el => el.value = {self.account}")
            await page.Jeval(Selectors.password, f"el => el.value = {password}")
            await page.Jeval(Selectors.captcha_txt, f"el => el.value = {code}")
            await page.click(Selectors.valid_thru_3h)

            await page.waitFor(random.randrange(500, 1000))

            # wait until login complete
            await asyncio.gather(
                *[
                    # submit the form
                    page.click(Selectors.login_button),
                    page.waitForNavigation(),
                ],
                return_exceptions=False,
            )

            if page.url.find("/Trade/Buy") != -1:
                logger.info("login succeeded")
                self._is_authed = True

        except Exception as e:
            logger.exception(e)
            dt = datetime.datetime.now()
            screenshot = os.path.join(
                self.screenshot_dir,
                f"login_{dt.year}-{dt.month}-{dt.day}_{dt.hour:02d}{dt.minute:02d}.jpg",
            )
            await page.screenshot(path=screenshot)
            # login failed, simply redo
            await asyncio.sleep(self._decay_retry)
            self._decay_retry *= 1.2
            logger.warning("login failed, retrying...")
            await self.login()

    async def _hack_captcha(self, img_src: str):
        _, response = await self.goto(img_src)
        letters, *_ = self._model._learner.predict(await response.buffer())
        return "".join(letters)

    async def _get_quotation(self, code) -> Quotation:
        quotation_url = f"https://hsmarket.eastmoney.com/api/SHSZQuoteSnapshot?id={code}&market=SH&callback="

        try:
            _, response = await self.goto(quotation_url)
            jsonp = await response.text()

            quotation = json.loads(jsonp.replace("(", "").replace(");", ""))
            return Quotation(**quotation)
        except Exception as e:
            logger.exception(e)
            msg = f"failed to fetch quotation for {code}"
            raise FetchQuotationError(msg)

    async def _place_order_long(self, code: str, units: int, price: float):
        """[summary]

        只实现限价委托方式。限价委托代码为'B'

        Args:
            code ([type]): 股票代码，6位数字
            units (int): 将买入的股票手数(一手=100股)
        """
        page, _ = await self.goto("/Trade/Buy")

        # 输入股票代码
        await page.focus(Selectors.stockcode)
        await page.keyboard.type(code)
        await page.waitFor(300)
        await page.keyboard.press("Enter")

        # 输入委托方式:限价委托
        control = "div.select_showbox"
        option = "div.select_box>ul>li[data-value='B']"

        await self.select_from_dropdown(page, control, option)

        # 输入买入价
        await page.Jeval(Selectors.price, f"el => el.value = {price}")

        # 输入购买股票数量
        await page.Jeval(Selectors.shares, f"el => el.value = {units * 100}")

        logger.info("order %s 手数 %s", units, code)

        await page.click(Selectors.confirm_order)
        # todo: wait for jump, and take screenshot on failure

    def _calc_units(self, money: float, price: float, margin: float = 1.1):
        """计算给定资金量`money`和`price`，能买入多少手股份。

        为提高资金利用率，允许超买（由`margin`指定）。举例来说，如果资金为1万，股价为9.3，则不超买的，允许买入1000股，资金余额为7千。允许超买的情况下，将买入1100股，使用资金为10,230元，超出2.3%，在默认的`margin`(10%)以内。

        买入股票数还将被限制在可用资金(`portfolio.avail`)以内

        Args:
            money (float): [description]
            price (float): [description]
            margin : 允许超买额，介于[1，1.5]之间。1.5意味着允许超买50%，但不会超过当前可用资金。

        Returns:
            [type]: [description]
        """
        assert 1 <= margin <= 1.5
        avail = self._portfolio.avail
        money = min(money, avail)

        units = int(((money / price) // 100))

        lower_bound = units * price
        upper_bound = (units + 1) * price * 100

        if (money - lower_bound >= upper_bound - money) and upper_bound < min(
            money * margin, avail
        ):
            # closer to upper_bound
            return units + 1
        else:
            return units

    async def buy(self, request: request.Request) -> response.HTTPResponse:
        """[summary]

        Args:
            request (request.Request): [description]

        Returns:
            response.HTTPResponse: [description]
        """
        args = request.json
        money = args.get("money")
        units = args.get("units")
        price = args.get("price")
        code = args.get("code")

        if all([money is None, units is None]):
            return response.json(body=None, status=400)

        try:
            quotation = await self._get_quotation(code)

            await self._get_portfolio()

            # 计算可买手数
            price = price or quotation.topprice
            units = units or self._calc_units(money, price)

            await self._place_order_long(code, units, price)
            return response.json(
                body={"err": 0, "oder": {"code": code, "price": price, "units": units}}
            )
        except FetchQuotationError as e:
            return response.json(body={"err": -1, "code": code, "desc": e.message})
        except FetchPortfolioError as e:
            return response.json(body={"err": -1, "desc": e.message})
        except PlaceOrderError:
            return response.json(
                body={
                    "err": -1,
                    "desc": "failed to place order",
                    "order": {"code": code, "units": units, "price": price},
                }
            )

    async def _on_portfolio_response(self, resp: pp.network_manager.Response):
        try:
            if resp.url.find("queryAssetAndPositionV1") != -1:
                result = await resp.json()
                if result["Status"] == 0:
                    return result["Data"][0]
                else:
                    logger.warning("failed to get portfolio: %s", result["Status"])
        except Exception as e:
            logger.exception(e)

    async def _get_portfolio(self):
        """获取资金持仓"""
        try:
            page, _ = await self.goto(
                "Search/Position", self._on_portfolio_response, "position"
            )
            data = await self.wait_response("position")
            self._portfolio = Portfolio(**Portfolio.convert(data))
        except Exception as e:
            logger.exception(e)
            filename = f"portfolio_{datetime_as_filename()}.jpg"
            await self.screenshot(page, filename)

            raise FetchPortfolioError(account=self.account)

    async def get_portfolio(self, request: request.Request) -> response.HTTPResponse:
        await self._get_portfolio()
        return response.json(self._portfolio.as_dict())
