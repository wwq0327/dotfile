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

#源目录及文件
sources = [
    '/home/wyatt/.emacs.d',
    '/home/wyatt/.config/awesome',
    '/home/wyatt/.emacs',
    '/home/wyatt/.xinitrc',
    '/home/wyatt/.local/share/exaile',
    '/home/wyatt/.themes',
    '/home/wyatt/.vimrc',
    '/etc/yum.repos.d',
    '/home/wyatt/.gitconfig'
    ]

#目标目录
target = '/home/wyatt/git/dotfile'
#shell cmd
rsync = "rsync"
#参数2
arguments = "-av"

def sync():
    '''遍历sources 并执行同步操作'''
    for src in sources:
        cmd = "%s %s %s %s" % (rsync, arguments, src, target)

        ret = call(cmd, shell=True)
        if ret != 0:
            print "rsync failed"
            time.sleep(3)
        else:
            print 'rsync was succesful'

if __name__ == '__main__':
    sync()
