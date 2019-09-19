import os
from datetime import datetime
from random import randint


class Fileup:
    def __init__(self, file, exts=None, size=1024 * 1024, is_randomname=False):


        if exts is None:
            exts = {'png', 'jpg','jpeg'}
        self.file = file # 文件对象
        self.exts = exts # 文件类型
        self.size = size # 文件大小
        self.israndomname = is_randomname # 是否随机起名

    #文件上传
    def upload(self,dest):

        if not self.ctype():
            return -1 # 文件类型不符合
        if not self.csize():
            return -2# 文件大小不符合

        if self.israndomname:
            self.file_name = self.ranfile()
        else:
            self.file_name = self.file.name

        path = os.path.join(dest,self.file_name)

        self.write_file(path)
        return 1

    def ctype(self):
        ext = os.path.splitext(self.file.name)
        if len(ext) > 1 :
            ext = ext[1].lstrip('.') # 取 . 后的字符串
            if ext in self.exts:
                return True
            return False


    def csize(self):
        if self.size < 0:
            return False
        return self.file.size <= self.size

    def ranfile(self):
        filename = datetime.now().strftime('%y%m%d%H%M%S')+str(randint(1,100000))
        ext = os.path.splitext(self.file.name)
        ext = ext[1] if len(ext)>1 else ''
        filename += ext
        return filename

    def write_file(self,path):
        with open(path,'wb') as rd:
            if self.file.multiple_chunks():
                for chunk in self.file.chunks():
                    rd.write(chunk)
            else:
                rd.write(self.file.read())
