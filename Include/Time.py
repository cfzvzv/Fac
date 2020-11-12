# 从百度获取网络时间
import arrow as ar
import requests as req


class Time:
    def __init__(self):
        now = ar.now()
        url = 'https://www.baidu.com/'
        date = req.get(url).headers['Date'][:-4]
        date = ar.get(date, 'ddd, DD MMM YYYY HH:mm:ss')
        self.diff = now - date

    @property
    def now(self):
        return ar.now() - self.diff


if __name__ == '__main__':
    t = Time()
    print(t.now, ar.now())
