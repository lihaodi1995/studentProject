# -*- coding: utf-8 -*-

u"""
使用 Python 在内存中生成 zip 文件
@see http://www.kompato.com/in-memory-zip-in-python
"""

import os
import zipfile
import StringIO


class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()

    def appendFile(self, file_path, file_name=None):
        u"从本地磁盘读取文件，并将其添加到压缩文件中"

        if file_name is None:
            p, fn = os.path.split(file_path)
        else:
            fn = file_name

        c = open(file_path, "rb").read()
        self.append(fn, c)

        return self

    def append(self, filename_in_zip, file_contents):
        """Appends a file with name filename_in_zip and contents of
                  file_contents to the in-memory zip."""

        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        """Returns a string with the contents of the in-memory zip."""

        self.in_memory_zip.seek(0)

        return self.in_memory_zip.read()

    def writetofile(self, filename):
        """Writes the in-memory zip to a file."""

        f = file(filename, "wb")
        f.write(self.read())
        f.close()