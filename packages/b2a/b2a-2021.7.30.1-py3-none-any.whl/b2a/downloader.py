#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  downloader.py
@Date    :  2021/7/29
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import os
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Lock

import aigpy.cmdHelper
from requests import get, head
from tqdm import tqdm


class Downloader(object):
    def __init__(self, url, nums, file, headers):
        self.url = url
        self.num = nums
        self.name = file
        self.headers = headers
        self.size = self.__getSize__()
        self._blockSize = 3 * 1024 * 1024
        self._lock = Lock()
        self._bar = tqdm(total=self.size, desc="下载中", unit_scale=True)

    def __getSize__(self):
        r = head(self.url, headers=self.headers)
        while r.status_code == 302:
            self.url = r.headers['Location']
            r = head(self.url)
        return int(r.headers['Content-Length'])

    def __createFile__(self):
        fp = open(self.name, "wb")
        fp.truncate(self.size)
        fp.close()

    def down(self, start, end):
        try:
            headers = {'Range': 'bytes={}-{}'.format(start, end)}

            # stream = True 下载的数据不会保存在内存中
            r = get(self.url, headers=headers.update(self.headers), stream=True)
            content = r.content
            # 写入文件对应位置,加入文件锁
            self._lock.acquire()
            with open(self.name, "rb+") as fp:
                fp.seek(start)
                fp.write(content)
                self._bar.update(end - start)
                self._lock.release()
        except Exception as e:
            pass

    def run(self):
        try:
            self.__createFile__()

            part = self._blockSize
            allroute = self.size // self._blockSize
            pool = ThreadPoolExecutor(max_workers=self.num)
            futures = []
            for i in range(allroute):
                start = part * i
                # 最后一块
                if i == allroute - 1:
                    end = self.size
                else:
                    end = start + part - 1
                futures.append(pool.submit(self.down, start, end))
            wait(futures)
            return True
        except Exception as e:
            aigpy.cmdHelper.printErr("下载失败：" + str(e))
            return False
