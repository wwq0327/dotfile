#!/usr/bin/env python
#coding:utf-8
#用于备份wyatt电脑上配置数据，内容包含如下：
# - 目录：
#       - .emacs.d
#       - .config/awesome
#       - .local/share/exaile
#       - .themes
# - 文件：
#       - .emacs
#       - .xinitrc
#
# wwq0327 <wwq0327@gmail.com>
#

from subprocess import call
import sys
import time
import os

#源目录及文件
src2tardict = {
    '.emacs.d': '/home/wyatt/.emacs.d',
    'awesome' : '/home/wyatt/.config/awesome',
    '.emacs'  : '/home/wyatt/.emacs',
    '.xinitrc': '/home/wyatt/.xinitrc',
    'exaile'  : '/home/wyatt/.local/share/exaile',
    '.themes' : '/home/wyatt/.themes',
    }

#目标目录
#target = '/home/wyatt/pycode/confbak'
#shell cmd
rsync = "rsync"
#参数2
arguments = "-av"

def sync():
    '''遍历sources 并执行同步操作'''
    if not os.path.isdir('/home/wyatt/.config/awesome'):
        os.mkdir('/home/wyatt/.config/awesome')

    if not os.path.isdir('/home/wyatt/.local/share/exaile'):
        os.mkdir('/home/wyatt/.local/share/exaile')
        
    for src, tar in src2tardict.items():
        cmd = "%s %s %s %s" % (rsync, arguments, src, tar)

        ret = call(cmd, shell=True)
        if ret != 0:
            print "rsync failed"
            time.sleep(3)
        else:
            print 'rsync was succesful'

if __name__ == '__main__':
    sync()
