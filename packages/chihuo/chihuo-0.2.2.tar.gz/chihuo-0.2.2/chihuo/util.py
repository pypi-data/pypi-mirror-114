import types

import json

from asyncio.queues import Queue


def make_ctrl_queue(concurrency, loop=None):
    queue = Queue(concurrency, loop=loop)
    for _ in range(concurrency):
        queue._put(1)
    return queue


def serialize_json(task):
    return json.dumps(task, separators=(",", ":"), ensure_ascii=False)


async def aretry(async_func, times: int, *args, **kwargs):
    """Retry an asynchronous function for `times` times

    Params:
    async_func: an asynchronous function
    args: arguments for async_func
    kwargs: keyword arguments for async_func
    times: retry times
    """

    assert isinstance(async_func, (types.FunctionType, types.MethodType))

    # If times <= 0, we retry the async_func until it returns
    if times < 1:
        times = 1 << 31

    for i in range(times):
        try:
            return await async_func(*args, **kwargs)
        except Exception as err:
            if i + 1 == times:
                raise err
