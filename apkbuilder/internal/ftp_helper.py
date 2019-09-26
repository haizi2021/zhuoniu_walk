#!/usr/bin/python
# -*- coding:utf-8 -*-

import ftplib
import os


class Ftp:
    def __init__(self, debugLevel=2):
        self._ftp = ftplib.FTP()
        self._ftp.set_debuglevel(debugLevel)

    def open(self, host, username, password, port=21, ):
        self._ftp.connect(host, port)
        self._ftp.login(username, password)

    def close(self):
        self._ftp.close()

    def setDebugLevel(self, debugLevel):
        self._ftp.set_debuglevel(debugLevel)

    def mkdir(self, path):
        print '---------' + path
        # 必须要先pwd获取当前路径，最后再cwd回这个路径，否则会出现’550 Create directory operation failed.‘等一系列问题
        currentDir = None
        try:
            currentDir = self._ftp.pwd()
        finally:
            pass
        try:
            self._ftp.cwd(path)
        except ftplib.error_perm:
            try:
                self._ftp.mkd(path)
            except ftplib.error_perm:
                print "WARNING: U have no authority to make dir"
        finally:
            if currentDir is not None:
                self._ftp.cwd(currentDir)

    def mkdirs(self, path):
        def dirname(path):
            return os.path.dirname(path)

        names = [path]
        name = path
        while True:
            name = dirname(name)
            if name is '':
                break
            names.append(name)
        names.reverse()
        for name in names:
            self.mkdir(name)

    def downloadfile(self, remotepath, localpath):
        '''从ftp下载文件'''
        bufsize = 1024
        fp = open(localpath, 'wb')
        self._ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        fp.close()

    def uploadfile(self, remotepath, localpath):
        '''从本地上传文件到ftp'''
        self.mkdirs(os.path.dirname(remotepath))
        bufsize = 1024
        with open(localpath, 'rb') as fp:
            ret = self._ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        return 'ftp://{}:{}/{}'.format(self._ftp.host, self._ftp.port, remotepath.lstrip('/'))


if __name__ == '__main__':
    pass
