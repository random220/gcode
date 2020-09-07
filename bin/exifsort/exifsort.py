#!/home/om/.local/share/virtualenvs/om-kFH46iaM/bin/python
import re
import os,sys
from exif import Image

def main():
    fromroot = '/shares/data/memories/Blackmachine-under-om-desk'
    toroot   = '/shares/data/memories/SORTED'

    for dirName, subdirList, fileList in os.walk(fromroot):
        for fileBaseName in fileList:
            filename = dirName+'/'+fileBaseName
            doit(filename)

def doit(filename):
    if not os.path.isfile(filename):
        sys.exit(1)
    size = os.path.getsize(filename)

    extn = ''
    m = re.search(r'\.([^\.]+)$', filename)
    if m:
        extn = m.group(1)

    with open(filename, 'rb') as f:
       i = Image(f)
       try:
           dt = i.datetime
           # 2015:11:27 15:21:37
       except KeyError:
           print(f'NODATE: {filename}')
           return

       m = re.search(r'^(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)$', dt)
       if m:
           (Y,M,D, h,m,s) = m.groups()
       else:
           print(f'NO-GOOD-DATE: {filename}')
           return

       dest_dirname  = f'/shares/data/memories/sorted/{Y}-{M}-{D}'
       cwd = os.getcwd()
       dest_dirname  = f'{cwd}/shares/data/memories/sorted/{Y}-{M}-{D}'
       dest_basename = f'{h}-{m}-{s}-size-{size}.{extn}'
       dest = f'{dest_dirname}/{dest_basename}'
       if os.path.isfile(dest):
           print(f'DUPE {dest} : {filename}')
           return

       if not os.path.isdir(dest_dirname):
           try:
               os.makedirs(dest_dirname, exist_ok=True)
           except:
               print(f'ERROR: failed to create directory {dest_dirname}')
               sys.exit(1)

       try:
           os.link(filename, dest)
       except:
           print(f'HARDLINKERROR: {filename}, {dest}')
           return

       os.unlink(filename)


main()
