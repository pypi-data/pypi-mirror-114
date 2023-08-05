import asyncio
import logging
import os

import aiofiles
import aiohttp
import fire
from hacktcha.model import HacktchaModel
from sanic.app import Sanic

from em.api import EMTraderWebInterface

app = Sanic("Eastmoney Trade Interface")
logger = logging.getLogger(__name__)


async def download_model(save_to: str):
    url = os.environ.get("hacktcha_model", None)
    if url is None:
        url = "https://stocks.jieyu.ai/models/hacktcha-vgg19_bn-4-10-1.00.pkl"
        logger.warning("env hacktcha_model is not set, use default: %s", url)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(save_to, mode="wb")
                await f.write(await response.read())
                await f.close()


async def create_hacktcha_model():
    """create hacktcha prediction model"""
    _dir = os.path.expanduser("~/em/models/")
    save_to = os.path.join(_dir, "hacktcha_model.pkl")
    if len(os.listdir(_dir)) == 0:
        await download_model(save_to)

    vocab = "0123456789"
    nletters = 4

    return HacktchaModel.from_model(save_to, vocab, nletters)


def serve(port: int = 3600):
    model = asyncio.run(create_hacktcha_model())
    em = EMTraderWebInterface(model)

    app.add_route(em.buy, "/em/buy", methods=["POST"])
    app.add_route(em.get_portfolio, "/em/portfolio", methods=["GET"])

    app.register_listener(em.init, "before_server_start")
    app.run(host="0.0.0.0", port=port, register_sys_signals=True)


if __name__ == "__main__":
    fire.Fire({"serve": serve})
