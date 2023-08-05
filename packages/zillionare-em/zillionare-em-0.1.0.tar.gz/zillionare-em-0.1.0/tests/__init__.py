"""Unit test package for em."""
import asyncio
import logging
import os
import socket
import subprocess
import sys
from contextlib import closing

import aiohttp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def asyncrun(func):
    async def setup_and_run(self):
        if getattr(self, "asyncSetup", None):
            await self.asyncSetup()

        try:
            await func(self)
        finally:
            if getattr(self, "asyncTearDown", None):
                await self.asyncTearDown()

    def wrapper(self):
        return asyncio.run(setup_and_run(self))

    return wrapper


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("localhost", 0))
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = s.getsockname()[1]
        return port


async def start_server(timeout=60):
    _server = os.path.join(os.path.dirname(__file__), "../em/server.py")
    server = os.path.normpath(_server)

    port = find_free_port()
    proc = subprocess.Popen(
        [sys.executable, server, "serve", f"--port={port}"],
        stdout=subprocess.DEVNULL,
    )

    for i in range(timeout, 0, -1):
        await asyncio.sleep(1)
        if await is_local_server_alive(port):
            logger.info("server started at %s", port)
            return proc, port

    raise subprocess.TimeoutExpired(cmd="serve", timeout=timeout)


async def is_local_server_alive(port):
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(f"http://localhost:{port}/em/portfolio") as resp:
                if resp.status == 200:
                    return True
    except Exception as e:
        pass

    return False
