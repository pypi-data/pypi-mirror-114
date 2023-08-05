#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys,importlib,os,shutil
import sztutil.tool as szt

szt目录="/mnt/n2n2_in/w/it/szt/data"
接收目录="recv"
发送目录="send"
'''
注意以上变量需要根据自己的情况进行调整
这个脚本是个示例脚本，仅适用于深证通数据收、发目录在一个大的数据目录下，每一个对端的收、发目录在同一个目录下而且不同的对端收、发目录同名。
脚本的功能就是检查所有的接收目录，如果有对方发来的需要自动处理的文件，则进行相应的自动处理。
目前支持的自动处理如下：


'''

class main(object):
    def __init__(self):
        self.findrecv(szt目录)
    def findrecv(self,ddir):
        if not os.path.isdir(ddir):
            return
        for f in os.listdir(ddir):
            ndir=os.path.join(ddir,f)
            if f==接收目录:
                sdir=os.path.join(ddir,发送目录)
                szt.checkrecv(ndir,sdir)
            elif os.path.isdir(ndir):
                self.findrecv(ndir)

if __name__ == "__main__":
    main()
