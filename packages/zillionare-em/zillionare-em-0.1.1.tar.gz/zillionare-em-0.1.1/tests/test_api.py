#!/usr/bin/env python
"""Tests for `em` package."""
# pylint: disable=redefined-outer-name

import asyncio
import unittest

from em.api import EMTraderWebInterface
from em.server import create_hacktcha_model
from tests import asyncrun, start_server
from em.quotation import Quotation
from unittest import mock
from em.server import app
import aiohttp


class TestApi(unittest.TestCase):
    async def asyncSetup(self):
        self.loop = asyncio.get_running_loop()
        self.model = await create_hacktcha_model()
        self.api = EMTraderWebInterface(self.model)
        await self.api.init()

        proc, port = await start_server()
        self.proc = proc
        self.port = port

    async def asyncTearDown(self):
        await self.api.stop()
        if self.proc:
            self.proc.kill()

    @asyncrun
    async def test_get_portfolio(self):
        await self.api._get_portfolio()
        self.assertTrue(self.api.portfolio is not None)

    @asyncrun
    async def test_get_quotation(self):
        q = await self.api._get_quotation("600000")
        self.assertEqual("600000", q.code)
        self.assertTrue(q.bottomprice > 0)

        q = Quotation()
        print(q.current_price)

    @asyncrun
    async def test_calc_shares(self):
        with mock.patch.object(self.api.portfolio, "avail", 10500):
            units = self.api._calc_units(10000, 9.3)
            self.assertEqual(11, units)

            units = self.api._calc_units(10000, 9.3, 1)
            self.assertEqual(10, units)

        with mock.patch.object(self.api.portfolio, "avail", 10100):
            units = self.api._calc_units(10000, 9.3)
            self.assertEqual(10, units)

        with mock.patch.object(self.api.portfolio, "avail", 9700):
            units = self.api._calc_units(10000, 9.3)
            self.assertEqual(10, units)

        with mock.patch.object(self.api.portfolio, "avail", 9100):
            units = self.api._calc_units(10000, 9.3)
            self.assertEqual(9, units)

    @asyncrun
    async def test_get_portfolio(self):
        resp = await self.api.get_portfolio(None)
        print(resp)

    @asyncrun
    async def test_buy(self):
        code = "600000"
        money = 10000
        price = 9.3

        async with aiohttp.ClientSession() as client:
            async with client.post(
                f"http://localhost:{self.port}/em/buy",
                json={"code": code, "money": money, "price": price},
            ) as resp:
                print(resp)
