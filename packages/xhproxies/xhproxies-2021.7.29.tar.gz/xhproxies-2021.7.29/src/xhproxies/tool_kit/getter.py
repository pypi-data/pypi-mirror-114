# -*- coding:utf-8 -*-
# @Author  : Creat by Han

from src.xhproxies.tool_kit.crawler import Crawler


class Getter():
    def __init__(self):
        self.crawler = Crawler()

    def run(self):
        print('获取器开始执行')
        all_proxies = []
        for callback_label in range(self.crawler.__CrawlFuncCount__):
            callback = self.crawler.__CrawlFunc__[callback_label]
            # 获取代理
            all_ip = self.crawler.get_proxies(callback)
            all_proxies.extend(all_ip)
        return all_proxies


if __name__ == '__main__':
    get = Getter()
    proxies = get.run()
