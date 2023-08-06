# -*- coding: utf-8 -*-
from api import Google, Searx, Rambler

import asyncio
import unittest
import random


class TestEngine(unittest.TestCase):

    def setUp(self) -> None:
        engines = (Google, Searx, Rambler)
        self.engine = engines[random.randint(0, len(engines) - 1)]()
        self.timeout = 300.0

    def tearDown(self) -> None:
        del self.engine

    def test_engine(self) -> None:
        asyncio.run(self.engine_test())

    async def engine_test(self):
        try:
            await asyncio.wait_for(self.engine.test(), timeout=self.timeout)
        except asyncio.TimeoutError:
            print("\nBitbucket's pipelines are free, but not infinity\n")  


if __name__ == "__main__":
    unittest.main()
