import asyncio
import unittest

from em.basecrawler import BaseCrawler, ResponseInterceptor
from tests import asyncrun


class TestBasecrawler(unittest.TestCase):
    async def asyncSetup(self):
        pass

    @asyncrun
    async def test_response_interceptor(self):
        crawler = BaseCrawler("https://www.baidu.com")

        async def on_response(resp):
            if (
                resp.request.url
                == "https://www.baidu.com/img/flexible/logo/pc/result.png"
            ):
                return await resp.buffer()

        await crawler.start()
        await crawler.goto(crawler.base_url, on_response, "test")
        resp = await crawler.wait_response("test", 2)
        self.assertEqual(6617, len(resp))

        await crawler.goto(crawler.base_url, on_response)
        await crawler.stop()
