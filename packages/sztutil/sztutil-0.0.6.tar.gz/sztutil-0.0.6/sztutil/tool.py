#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,inspect,shutil,time

def createok(filename):
    f=open("%s.ok" %(filename),"w")
    f.write("ok")
    f.close()

class checkrecv(object):    #检查接收目录判断是否需要自动处理
    def __init__(self,rdir,sdir):
        self.rdir=rdir
        self.sdir=sdir
        if not os.path.isdir(rdir):return
        if not os.path.isdir(sdir):return
        self.check()
    def check(self):
        for f in os.listdir(self.rdir):
            fl=f.lower()
            if not fl.endswith(".rcv"):continue
            if fl.find("auto")<0:continue
            for i in vars(checkrecv):
                if i.startswith("__"):
                    continue
                fun=getattr(checkrecv,i)
                if inspect.isfunction(fun) and fl.find(i)>=0:
                    os.remove(os.path.join(self.rdir,f))
                    f2=os.path.join(self.rdir,f[:-4])
                    fun(self,f2)

    def autohelp(self,f):
        helpfile=os.path.join(os.path.dirname(os.path.abspath(__file__)),"datafile","sztutil_manual.txt")
        tf=os.path.join(self.sdir,"sztutil_manual.txt")
        shutil.copy2(helpfile,tf)
        shutil.copy(helpfile,tf+".ok")

    def autofilelist(self,f):
        self.文件列表=[]
        self.updatesendlist(self.sdir)  #更新文件列表
        self.文件列表.sort()
        f=open("%s/retfilelist.txt" %(self.sdir),"w")
        for t in self.文件列表:
            f.write(t+"\n")
        f.close()
        createok("%s/retfilelist.txt" %(self.sdir))
    
    def updatesendlist(self,sdir):
        for f in os.listdir(sdir):
            f=os.path.join(sdir,f)
            if os.path.isdir(f):
                self.updatesendlist(f)
            else:
                if f.endswith(".snt"):continue
                if f.endswith(".ok"):continue
                st=os.stat(f)
                mtime=time.strftime('%Y%m%d%H%M%S',time.localtime(st.st_mtime))
                self.文件列表.append("%s %s %d" %(f[len(self.sdir)+1:],mtime,st.st_size))
    
    def autogetfile(self,f):
        f=open(f)
        for ff in f.readlines():
            ff=ff.split()
            if(len(ff)==0):continue
            ff=os.path.join(self.sdir,ff[0])
            if not os.path.isfile(ff):continue
            createok(ff)
        f.close()

class autosend(object):
    def __init__(self,stdata,storidata):
        self.接收目录=stdata["接收目录"]
        self.发送目录=stdata["发送目录"]
        self.findrecv(stdata["目录"])
    def findrecv(self,ddir):
        if not os.path.isdir(ddir):
            return
        for f in os.listdir(ddir):
            ndir=os.path.join(ddir,f)
            if f==self.接收目录:
                sdir=os.path.join(ddir,self.发送目录)
                checkrecv(ndir,sdir)
            elif os.path.isdir(ndir):
                self.findrecv(ndir)
