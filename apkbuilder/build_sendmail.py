#!/usr/bin/python
# -*- coding:utf-8 -*-

import codecs
import webbrowser
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from internal import git_helper

'''<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style>
table{border-right:1px solid #ccc;border-bottom:1px solid #ccc} 
table td{border-left:1px solid #ccc;border-top:1px solid #ccc;padding-left:8px;padding-right:8px;} 
*{font-size:14px; }
.important_text{color:#369; font-weight: bold;}
.log_info{color:#000; }
.normal_info{color:#666; }
.maintitle{font-size: 18px;}
.title{background-color:#369; border:1px solid #369; color:#fff}
    </style>
</head>
<body>
<div><br/> <br/> <br/></div>

<table style='line-height:28px' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td align='center' rowspan='5' class='maintitle' width='25%'>测试包详情</td>
        <td class='maintitle' width='25%'>GO输入法主包</td>
        <td width='50%'><span class='important_text'>"${SVN_CODE}"</span></td>
    </tr>
</table>

<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td class='normal_info' width='25%'>svn地址</td>
        <td class='important_text' width='75%'><a href='"${APK_LINK}"'>"${APK_LINK}"</a></td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>类型</td>
        <td class='important_text' width='75%'>"${APK_TYPE}"</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>渠道</td>
        <td class='important_text' width='75%'>"${CHANNEL_CODE}"</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>VersionCode</td>
        <td width='75%' class='important_text'>"${VERSION_CODE}"</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>VersionName</td>
        <td width='75%' class='important_text'>"${VERSION_NAME}"</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>打包日期</td>
        <td width='75%'>"${PACKAGE_DATE}"</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>文件大小(Byte)</td>
        <td width='75%'>${PACKAGE_SIZE}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>备注</td>
        <td width='75%'>${DEX_INFO}</td>
    </tr>
</table>

<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td align='center' colspan='4' class='title' width='100%'>更新说明</td>
    </tr>

    <tr style="background-color:gray">
        <td align='center' width='10%'>序号</td>
        <td align='center' width='40%'>功能</td>
        <td align='center' width='30%'>状态</td>
        <td align='center' width='20%'>负责人</td>
    </tr>
    <tr>
        <td align='center' width='10%'>"$order"</td>
        <td align='center' width='40%'>"$func"</td>

        <td align='center' width='30%'>"$state"</td>

        <td align='center' width='20%'>"$name"</td>
    </tr>
    <tr>
        <td align='center' width='10%'>"$order"</td>
        <td align='center' width='40%'>"$func"</td>

        <td style="background-color:yellow" align='center' width='30%'>"$state"</td>

        <td align='center' width='20%'>"$name"</td>
    </tr>

    <tr>
        <td align='center' width='10%'>"$order"</td>
        <td align='center' width='40%'> </td>
        <td align='center' width='30%'> </td>
        <td align='center' width='20%'> </td>
    </tr>
</table>

<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td align='center' colspan='3' class='title' width='100%'>测试重点</td>
    </tr>
    <tr>
        <td>
            </br>
            </br>
            </br>
        </td>
    </tr>
</table>

<table></table>
</body>
</html>
'''


class SendMail:
    def __init__(self,
                 build_project_root='.',
                 build_produce_name='PhotoEdit',
                 build_info='1.0.0-10-201711111111',
                 build_apk_address='ftp://127.0.0.1',
                 build_type='release',
                 build_channel='',
                 build_versionCode=10,
                 build_versionName='1.0.0',
                 build_package_date='',
                 build_package_size='',
                 build_remark='',  # 备注
                 build_produce_demand_file='build_product_demand.txt',
                 build_produce_demand=[],
                 build_test_details_file='build_test_details.txt',
                 build_test_details=[],
                 build_version_commit_count=20,
                 ):
        self._currentDir = os.path.dirname(os.path.abspath(__file__))

        self._build_project_root = build_project_root
        self._build_version_commit_count = build_version_commit_count
        self._build_test_details = build_test_details
        self._build_test_details_file = os.path.join(self._currentDir, build_test_details_file)
        self._build_produce_demand = build_produce_demand
        self._build_produce_demand_file = os.path.join(self._currentDir, build_produce_demand_file)
        self._build_remark = build_remark
        self._build_package_size = build_package_size
        self._build_package_date = build_package_date
        self._build_versionName = build_versionName
        self._build_versionCode = build_versionCode
        self._build_channel = build_channel
        self._build_type = build_type
        self._build_apk_address = build_apk_address
        self._build_info = build_info
        self._build_produce_name = build_produce_name

        self._lines = []

    def _addProduceDemand(self):
        infos = [u'''<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
                                                                                                                     <tr>
                                                                                                                     <td align='center' colspan='4' class='title' width='100%'>产品需求</td>
    </tr>

    <tr style="background-color:gray">
        <td align='center' width='10%'>序号</td>
        <td align='center' width='40%'>功能</td>
        <td align='center' width='30%'>状态</td>
        <td align='center' width='20%'>负责人</td>
    </tr>
</tr>''']
        order = 0
        with codecs.open(self._build_produce_demand_file, 'r', 'utf-8') as fp:
            for line in fp:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue

                # 功能1_提测_kun
                cols = line.split('_')
                if len(cols) != 3:
                    raise Exception('产品需求未按要求格式填写...')
                func, state, name = cols
                order += 1
                item = ''
                if state == u'提测':
                    item = u'''<tr>
        <td align='center' width='10%'>{order}</td>
        <td align='left' width='50%'>{func}</td>
        <td align='center' width='20%'>{state}</td>
        <td align='center' width='20%'>{name}</td>
    </tr>'''
                else:
                    item = u'''<tr>
        <td align='center' width='10%'>{order}</td>
        <td align='left' width='50%'>{func}</td>
        <td style="background-color:yellow" align='center' width='20%'>{state}</td>
        <td align='center' width='20%'>{name}</td>        
    </tr>'''
                infos.append(item.format(order=order, func=func, state=state, name=name))

        infos.append(u'''<tr>
        <td align='center' width='10%'> </td>
        <td align='center' width='50%'> </td>
        <td align='center' width='20%'> </td>
        <td align='center' width='20%'> </td>
    </tr>''')
        infos.append(u'''
</table>''')
        return infos

    def _addTestDetails(self):
        infos = [u'''<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td align='center' colspan='3' class='title' width='100%'>测试重点</td>
    </tr>
    <tr>
        <td>''']
        with codecs.open(self._build_test_details_file, 'r', 'utf-8') as fp:
            for line in fp:
                line = line.strip()
                if line.startswith('#') or len(line) == 0:
                    continue
                infos.append(line + u'</br>')
        infos.append(u'''</td>
    </tr>
</table>''')
        return infos

    def _addVersionCommit(self):

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
        git_record = git_helper.getGitVersionCommit(self._build_project_root,
                                                    commitCount=self._build_version_commit_count)
        if len(git_record) > 0:
            record = []
            for branchInfo in git_record:
                record.append(u'''<tr style="background-color:gray">
                <td colspan='3' width='100%'>[{type}] {path}======>{branch}</td>
                </tr>'''.format(type=branchInfo['type'],
                                path=branchInfo['path'],
                                branch=branchInfo['branch']))

                for commit in branchInfo['commits']:
                    record.append(u'''<tr>
            <td align='center' width='20%'>{committer}</td>
            <td align='center' width='20%'>{version}</td>
            <td align='center' width='40%'>{time}</td>
        </tr>'''.format(committer=commit['committer'],
                        version=commit['version'],
                        time='{0}({1})'.format(commit['time'], commit['timeago'])))
                    record.append("<tr><td colspan='3' width='100%'>" + commit['info'].replace('\n', '<br/>').decode(
                        'utf8') + '</td></tr>')
            info = u''.join(record)
        infos = [u'''<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
                    <tr>
                        <td align='center' colspan='3' class='title' width='100%'>提交记录</td>
                    </tr>
                     <tr>
                     ''',
                 info,
                 u'''
             </tr>
         </table>''']

        return infos

    def build(self):
        self._lines = []
        # add header
        header = u'''<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style>
table{border-right:1px solid #ccc;border-bottom:1px solid #ccc} 
table td{border-left:1px solid #ccc;border-top:1px solid #ccc;padding-left:8px;padding-right:8px;} 
*{font-size:14px; }
.important_text{color:#369; font-weight: bold;}
.log_info{color:#000; }
.normal_info{color:#666; }
.maintitle{font-size: 18px;}
.title{background-color:#369; border:1px solid #369; color:#fff}
    </style>
</head>
    <body>
    <div><br/> <br/> <br/></div>'''

        title = u'''<table style='line-height:28px' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td align='center' rowspan='5' class='maintitle' width='25%'>测试包详情</td>
        <td class='maintitle' width='25%'>{BUILD_PRODUCE_NAME}</td>
        <td width='50%'><span class='important_text'>{BUILD_INFO}</span></td>
    </tr>
</table>'''.format(BUILD_PRODUCE_NAME=self._build_produce_name, BUILD_INFO=self._build_info)

        packageInfo = u'''<table style='line-height:28px;margin-top:10px;' cellpadding='0' cellspacing='0' width='800'>
    <tr>
        <td class='normal_info' width='25%'>apk地址</td>
        <td class='important_text' width='75%'><a href='{BUILD_APK_ADDRESS}'>{BUILD_APK_ADDRESS}</a></td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>类型</td>
        <td class='important_text' width='75%'>{BUILD_TYPE}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>渠道</td>
        <td class='important_text' width='75%'>{BUILD_CHANNEL}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>VersionCode</td>
        <td width='75%' class='important_text'>{BUILD_VERSIONCODE}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>VersionName</td>
        <td width='75%' class='important_text'>{BUILD_VERSIONNAME}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>打包日期</td>
        <td width='75%'>{BUILD_PACKAGE_DATE}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>文件大小(Byte)</td>
        <td width='75%'>{BUILD_PACKAGE_SIZE}</td>
    </tr>
    <tr>
        <td class='normal_info' width='25%'>备注</td>
        <td width='75%'>{BUILD_REMARK}</td>
    </tr>
</table>'''.format(BUILD_APK_ADDRESS=self._build_apk_address,
                   BUILD_TYPE=self._build_type,
                   BUILD_CHANNEL=self._build_channel,
                   BUILD_VERSIONCODE=self._build_versionCode,
                   BUILD_VERSIONNAME=self._build_versionName,
                   BUILD_PACKAGE_DATE=self._build_package_date,
                   BUILD_PACKAGE_SIZE=self._build_package_size,
                   BUILD_REMARK=self._build_remark, )

        # add tail
        tail = ''' </body>
</html>'''

        self._lines.append(header)
        self._lines.append(title)
        self._lines.append(packageInfo)
        self._lines.extend(self._addProduceDemand())
        self._lines.extend(self._addTestDetails())
        self._lines.extend(self._addVersionCommit())
        self._lines.append(tail)

        return u''.join(self._lines)

    def buildAndSendmail(self, mailTo, mailCC, title, username, password):
        info = self.build()
        try:
            info = info.replace('"', '\'')
            info = info.encode('utf8')
        finally:
            pass

        mailFrom = username  # 发件人邮箱账号
        ret = True
        try:
            msg = MIMEText(info, 'html', 'utf-8')
            msg['From'] = formataddr(["test", mailFrom])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr([None, mailTo])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = title  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(username, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(mailFrom, [mailTo, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            print 'send mail to ' + mailTo
        except Exception, e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print e
        return ret


def browser(buf):
    try:
        buf = buf.encode('utf-8')
    except Exception, e:
        pass
    tmpfile = 'tmp_sendmail.html'
    with open(tmpfile, 'w') as fp:
        fp.write(buf)

    webbrowser.open(tmpfile)


if __name__ == '__main__':
    sendMail = SendMail(build_project_root='.',
                        build_produce_name='PhotoEdit',
                        build_info='1.0.0-10-201711111111',
                        build_apk_address='ftp://127.0.0.1',
                        build_type='release',
                        build_channel='',
                        build_versionCode=10,
                        build_versionName='1.0.0',
                        build_package_date=time.strftime('%Y-%m-%d %H:%M:%S',
                                                         time.localtime(time.time())),
                        build_package_size='123456',
                        build_remark=u'备注',  # 备注
                        build_produce_demand_file='build_product_demand.txt',
                        build_test_details_file='build_test_details.txt',
                        build_version_commit_count=10
                        )
    info = sendMail.build()
    browser(info)
    title = '[test]{projectName}-{versionName}-{versionCode}' \
        .format(projectName='PhotoEdit',
                versionName='1.0.0',
                versionCode=10)
    MAIL_TO = 'zhaokun@himobi.net'
    MAIL_CC = ''
    MAIL_USERNAME = 'jira@himobi.net'
    MAIL_PASSWORD = 'Zn123456'
    # sendMail.buildAndSendmail(mailTo=MAIL_TO, mailCC=MAIL_CC, title=title, username=MAIL_USERNAME,
    #                           password=MAIL_PASSWORD)

    # print getGitVersionCommit(r'D:\work\workspace\camera\PhotoEdit', '\n')
