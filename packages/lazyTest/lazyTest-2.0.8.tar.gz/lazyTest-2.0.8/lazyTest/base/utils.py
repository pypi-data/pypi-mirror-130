# -*- coding = UTF-8 -*-
# Author   : xingHeYang
# time     : 2021/11/30 21:38
# ---------------------------------------
import functools


import lazyTest


def _retrying(func):
    @functools.wraps(func)
    def inner(*args):
        lazyTest.logger.debug(f"传入的selector为：{args[1]}")
        if isinstance(args[1], str):
            lazyTest.logger.debug("字符串不进行重试")
            result = func(*args)
            return result
        ele = iter(args[1])

        def run(ele, *args):
            args = list(args)  # 兼容多个参数
            try:
                e = next(ele)
                lazyTest.logger.debug(f"元素重试机制-->尝试定位：{e}")
            except StopIteration:
                raise Exception(f"元素重试结束，无法定位：{args}")
            try:
                args[1] = e  # 处理时只处理第一个参数
                result = func(*args)
                return result
            except BaseException as e:  # 捕获所有异常
                result = run(ele, *args)
            return result

        result = run(ele, *args)
        return result

    return inner


def Retrying(num: int = 2):
    """
    操作执行重试，默认重试3次，3次后依然报错则判断失败
    :param num: 默认重试次数3
    :return: 无
    """

    def retrying(func):
        nonlocal num

        @functools.wraps(func)
        def inner(*args, **kwargs):
            nonlocal num
            lazyTest.logger.debug(f"动作重试机制生效，总重试次数：{num}")

            @lazyTest.Sleep(1)
            def run(num, *args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return result
                except BaseException:
                    if num == 0:
                        raise Exception("动作重试结束，无法完成指定动作")
                    lazyTest.logger.error(f"动作执行失败，重试")
                    num -= 1
                    run(num, *args, **kwargs)

            result = run(num, *args, **kwargs)
            return result

        return inner

    return retrying
