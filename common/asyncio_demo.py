#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : asyncio_test.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2020-12-25 15:40 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

import asyncio
import time
import random


async def count(n):
    print(f"{n}: One")
    await asyncio.sleep(abs(10 - n))
    print(f"{n}: Two")


async def count_n(n):
    for i in range(n):
        print(f'{n}-{i}, sleep 1 second')
        await asyncio.sleep(1)


async def chain(n):
    start = time.perf_counter()
    print(f'start chain task-{n}')
    await asyncio.gather(count(n), count(n))
    await count_n(n)
    end = time.perf_counter() - start
    print(f'end chain task-{n} in {end} seconds')


async def main(*args):
    await asyncio.gather(*(chain(i) for i in args))


asyncio.run(main(3, 6))
