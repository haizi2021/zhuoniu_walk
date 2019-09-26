#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def _popen(cmd):
    return os.popen(cmd)


def getUserName():
    return _popen('git config user.name').read().strip()


def getUserEmail():
    return _popen('git config user.email').read().strip()


def getGitVersionCommit(path, commitCount=10):
    '''
%H	提交对象（commit）的完整哈希字串
%h	提交对象的简短哈希字串
%T	树对象（tree）的完整哈希字串
%t	树对象的简短哈希字串
%P	父对象（parent）的完整哈希字串
%p	父对象的简短哈希字串
%an	作者（author）的名字
%ae	作者的电子邮件地址
%ad	作者修订日期（可以用 -date= 选项定制格式）
%ar	作者修订日期，按多久以前的方式显示
%cn	提交者(committer)的名字
%ce	提交者的电子邮件地址
%cd	提交日期
%cr	提交日期，按多久以前的方式显示
%s	提交说明

    :param path:
    :return:
    '''
    prevDir = os.curdir
    os.chdir(path)

    '''
    [
        {
            'type': "main",
            'path': ''
            'branch': 'pe1.06'
            'commits': [{'committer': committer,
                        'version': code,
                        'time': time,
                        'timeago': timeago,
                        'info': info},
                        ]
        },
        {
            'type': "submodule",
            'path': 'third_party/CommercializeSDK'
            'branch': 'pe1.06'
            'commits': [{'committer': committer,
                        'version': code,
                        'time': time,
                        'timeago': timeago,
                        'info': info},
                        ]
        }
        
    ]
    '''
    infos = []

    def getSubmodulePath(line):
        return line.strip().replace('Entering', '').replace('正在进入','').strip().strip('\'')

    def getGitLog(commitCount=20, submodule=False):
        currentSubmodulePath = 'main'
        projectCommits = {currentSubmodulePath: []}
        cmd = 'git log -{commitCount} --pretty=format:"<%cn><%h><%cd><%cr><%s>"'
        if submodule:
            projectCommits = {}
            cmd = '''git submodule foreach "git log -{commitCount} --pretty=format:\<%cn\>\<%h\>\<%cd\>\<%cr\>\<%s\>"'''
        cmd = cmd.format(commitCount=commitCount)
        print cmd
        for line in os.popen(cmd):
            if line.strip().startswith('Entering') or line.strip().startswith('正在进入'):
                currentSubmodulePath = getSubmodulePath(line)
                projectCommits[currentSubmodulePath] = []
                continue
            cols = re.findall(r'<(.*?)><(.*?)><(.*?)><(.*?)><(.*?)>', line)
            if len(cols) == 1 and len(cols[0]) != 5:
                continue
            committer, code, time, timeago, info = cols[0]
            projectCommits[currentSubmodulePath].append({'committer': committer,
                                                         'version': code,
                                                         'time': time,
                                                         'timeago': timeago,
                                                         'info': info})
        return projectCommits

    # 当前分支
    currentBranchName = ''
    for line in os.popen('git branch'):
        if line.strip().startswith("*"):
            currentBranchName = line.replace('*', '').strip()
            break
    mainProjectInfo = {'type': "main", 'path': '', 'branch': currentBranchName}

    projectCommits = getGitLog(commitCount=commitCount, submodule=False)
    mainProjectInfo['commits'] = projectCommits['main']

    submoduleInfos = {}
    currentSubmodulePath = ''
    for line in os.popen('git submodule foreach "git branch"'):
        if line.strip().startswith('Entering') or line.strip().startswith('正在进入'):
            currentSubmodulePath = getSubmodulePath(line)
            submoduleInfos[currentSubmodulePath] = {
                'type': "submodule",
                'path': currentSubmodulePath,
                'branch': ''
            }
        elif line.strip().startswith("*"):
            currentBranchName = line.replace('*', '').strip()
            submoduleInfos[currentSubmodulePath]['branch'] = currentBranchName

    projectCommits = getGitLog(commitCount=commitCount, submodule=True)
    for key, value in projectCommits.iteritems():
        submoduleInfos[key]['commits'] = value

    os.chdir(prevDir)

    ret = [mainProjectInfo]
    ret.extend(submoduleInfos.values())
    return ret;


if __name__ == '__main__':
    pass
