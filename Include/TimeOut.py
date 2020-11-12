import functools
from json import loads
from threading import Thread
from time import sleep

import arrow as ar

from Include.Path import Path


def timeout(timeout_):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout_))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e

            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout_)
            except Exception as je:
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret

        return wrapper

    return deco


def trade_time():
    holiday = loads(Path('Bin/Config/Holiday.json').text())
    tz = ar.now().tzinfo

    # everyday
    now = ar.now()
    everyday_close_time, everyday_open_time = holiday['everyday'][0]
    everyday_close_time = f"{now.format('YYYY-MM-DD')} {everyday_close_time}"
    everyday_open_time = f"{now.format('YYYY-MM-DD')} {everyday_open_time}"
    everyday_close_time = ar.get(everyday_close_time).replace(tzinfo=tz)
    everyday_open_time = ar.get(everyday_open_time).replace(tzinfo=tz)

    target_time = now
    if now.isoweekday() == 1 and now < everyday_open_time:  # 工作日
        target_time = everyday_open_time
    elif 2 <= now.isoweekday() <= 5 and everyday_close_time <= now < everyday_open_time:
        target_time = everyday_open_time
    elif now.isoweekday() == 6 and now > everyday_close_time:
        target_time = everyday_open_time.shift(days=2)
    elif now.isoweekday() == 7:
        target_time = everyday_open_time.shift(days=1)

    diff = target_time.float_timestamp - now.float_timestamp
    if diff > 0:
        print(f'常规休眠{diff}s,待{target_time}启动！')
        sleep(diff)

    # holiday
    for close_time, open_time in holiday['holiday']:
        now = ar.now()
        close_time = ar.get(close_time).replace(tzinfo=tz)
        open_time = ar.get(open_time).replace(tzinfo=tz)
        if close_time <= now < open_time:
            diff = open_time.float_timestamp - now.float_timestamp
            if diff > 0:
                print(f'节假日休眠{diff}s,待{open_time}启动！')
                sleep(diff)

    print('交易时间')
