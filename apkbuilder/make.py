#!/usr/bin/python
# -*- coding:utf-8 -*-

import getopt
import sys
import ftplib
import os
import re
import time
import build_sendmail
from internal import ftp_helper
from internal import git_helper

MAIL_TO = 'Android-T1@himobi.net'
MAIL_CC = ''
MAIL_USERNAME = 'jira@himobi.net'
MAIL_PASSWORD = 'Zn1234567'

FTP_HOST = '120.79.194.241'
FTP_USERNAME = 'test'
FTP_PASSWORD = 'zntest'


class Params:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:]
                                   , "hr:n:t:v:c:d:p:"
                                   , ["help"
                                       , 'projectDir='
                                       , 'projectName='
                                       , 'projectBuildType='
                                       , 'projectVersionName='
                                       , 'projectVersionCode='
                                       , 'projectBuildDate='
                                       , 'projectBuildApkPath='
                                       , 'commitCount='
                                      ])
        print opts
        print args
        self.projectDir = ''
        self.projectName = ''
        self.projectBuildType = 'release'
        self.projectVersionName = ''
        self.projectVersionCode = ''
        self.projectBuildDate = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        self.projectBuildApkPath = ''
        self.commitCount = 30
        for op, value in opts:
            if op in ["-h", '--help']:
                self.usage()
                sys.exit()
            elif op in ['-r', '--projectDir=', '--projectDir']:
                self.projectDir = value
            elif op in ["-n", '--projectName=', '--projectName']:
                self.projectName = value
            elif op in ["-t", '--projectBuildType=', '--projectBuildType']:
                self.projectBuildType = value
            elif op in ["-v", '--projectVersionName=', '--projectVersionName']:
                self.projectVersionName = value
            elif op in ["-c", '--projectVersionCode=' '--projectVersionCode']:
                self.projectVersionCode = value
            elif op in ["-d", '--projectBuildDate=', '--projectBuildDate']:
                self.projectBuildDate = value
            elif op in ["-p", '--projectBuildApkPath=', '--projectBuildApkPath']:
                self.projectBuildApkPath = value
            elif op in ['--commitCount=', '--commitCount']:
                self.commitCount = value
        # check
        if (self.projectDir is ''
            or self.projectName is ''
            or self.projectVersionName is ''
            or self.projectVersionCode is ''
            or self.projectBuildApkPath is ''
            ):
            self.usage()
            sys.exit()

    def usage(self):
        sys.stdout.write('''python make.py     
     -r or --projectDir=
     -n or --projectName=
     -t or --projectBuildType=  default release
     -v or --projectVersionName=
     -c or --projectVersionCode=
     -d or --projectBuildDate={projectBuildDate}
     -p or --projectBuildApkPath= 
     
     eg: python make.py -n PhotoEdit -t release -v 1.00.00 -c 20 -d 20171111 -p d://abc/def/aaa.apk
'''.format(projectBuildDate=self.projectBuildDate))


def main(params):
    # 开始上传
    ftp = ftp_helper.Ftp()
    ftp.open(FTP_HOST, FTP_USERNAME, FTP_PASSWORD)
    uploadFtpPath = '{0}/{1}/{2}'.format(params.projectName, params.projectVersionName,
                                         os.path.basename(params.projectBuildApkPath))
    print 'start upload to ' + uploadFtpPath
    filepath = ftp.uploadfile(uploadFtpPath, params.projectBuildApkPath)
    print 'upload path:' + filepath
    ftp.close()

    build_remark = u'提测人：{0}({1})'.format(git_helper.getUserName(), git_helper.getUserEmail())

    # send mail
    filesize = os.path.getsize(params.projectBuildApkPath)
    sendMail = build_sendmail.SendMail(
        build_project_root=params.projectDir,
        build_produce_name=params.projectName,
        build_info='{0}-{1}-{2}'.format(params.projectVersionName, params.projectVersionCode,
                                        params.projectBuildDate),
        build_apk_address=filepath,
        build_type=params.projectBuildType,
        build_channel='',
        build_versionCode=params.projectVersionCode,
        build_versionName=params.projectVersionName,
        build_package_date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        build_package_size=filesize,
        build_remark=build_remark,  # 备注
        build_produce_demand_file='build_product_demand.txt',
        build_test_details_file='build_test_details.txt',
        build_version_commit_count = params.commitCount,
    )

    # info = sendMail.build()
    # build_sendmail.browser(info)

    title = '[提测] {projectName}-{versionName}-{versionCode}' \
        .format(projectName=params.projectName,
                versionName=params.projectVersionName,
                versionCode=params.projectVersionCode)
    sendMail.buildAndSendmail(mailTo=MAIL_TO, mailCC=MAIL_CC, title=title, username=MAIL_USERNAME,
                              password=MAIL_PASSWORD)


'''
python apkbuilder/make.py -r . -n PhotoEdit -t release -v 1.00.00-test -c 20 -d 20171111 -p D:\work\workspace\camera
\PhotoEdit\out\PhotoEditor-release-1.08-18-201710312003\AndResGuard_PhotoEditor-release-1.08-18-201710312003\PhotoEditor-release-1.08-18-201710312003_signed_
7zip_aligned.apk

'''
if __name__ == '__main__':
    params = Params()
    main(params)

    # infos = getGitVersionCommit(r'D:\work\workspace\camera\PhotoEdit-old', 3)
    # for info in infos:
    #     print info
