# -*- coding: utf-8 -*-
"""

Search for .jpg .jpeg .jfif in given directory.
Adds to file's name prefix with the date of creation of the file.

@author: Lukasz
"""

from PIL import Image

import os
import re
import sys
#import time

CREATE_HARDLINK=0
from datetime import timedelta 
from datetime import datetime

def add_two_hours(datetime_str):
    datetime_object = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
    datetime_object += timedelta(hours=2)
    return datetime_object.strftime('%Y:%m:%d %H:%M:%S')
    
def extract_jpeg_exif_time(jpegfn):
    if not os.path.isfile(jpegfn):
        return None
    try:
        im = Image.open(jpegfn)
        if hasattr(im, '_getexif'):
            exifdata = im._getexif()
            ctime = exifdata[306]
            
            ctime = add_two_hours(ctime)
            
            return ctime
    except: 
        _type, value, traceback = sys.exc_info()
        print ("Error:\n%r", value)
    
    return None

def get_exif_prefix(jpegfn):
    ctime = extract_jpeg_exif_time(jpegfn)
    if ctime is None:
        return None
    ctime = ctime.replace(':', '')
    ctime = re.sub('[^\d]+', '_', ctime)
    return ctime

def rename_jpeg_file(fn):
    if not os.path.isfile(fn):
        return 0
    ext = os.path.splitext(fn)[1].lower()
#    if ext in ['.jpg', '.jpeg', '.jfif']:
    if ext not in ['.jpg', '.jpeg', '.jfif']:
        return 0
    path, base = os.path.split(fn)
    print (base) # status
    prefix = get_exif_prefix(fn)
    if prefix is None:
        return 0 

    base = 'aparat'
    new_name = prefix + '_' + base + '.jpg'
    new_full_name = os.path.join(path, new_name)

    name_ok = False # if the name already exist we add suffix _2
    n =1
    while(not name_ok):
        if CREATE_HARDLINK:
            f = open('CREATE_HARDLINK.cmd', 'a')
            f.write('fsutil hardlink create "%s" "%s"\n' % (new_full_name, fn))
            f.close()
        else:
            try:
                os.rename(fn, new_full_name)
                name_ok = True
                print('OK')
            except:                
                _type, value, traceback = sys.exc_info()
                print ("Error:\n%r", value)
        
        n += 1
        new_name = prefix + '_' + base + '_{}.jpg'.format(n)
        new_full_name = os.path.join(path, new_name)
    return 1

def rename_jpeg_files_in_dir(dn):
    names = os.listdir(dn)
    count=0
    for n in names:
        file_path = os.path.join(dn, n)
        count += rename_jpeg_file(file_path)
    return count


if __name__=='__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        path = r'C:\Pliki\Zdjęcia\2018.04.10-21 Gruzja\Lustrzanka Dawida\100MSDCF'

    if os.path.isfile(path):
        rename_jpeg_file(path)
    elif os.path.isdir(path):
        count = rename_jpeg_files_in_dir(path)
        print ('%d file(s) renamed.' % count)
    else:
        print ('ERROR: path not found: %s' % path)