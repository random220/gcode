#!/home/om/.local/share/virtualenvs/om-kFH46iaM/bin/python
import re
import os,sys
from exif import Image

class G:
    fromroot = '/shares/data/memories/Blackmachine-under-om-desk'
    toroot   = '/shares/data/memories/SORTED'

def main():

    if len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]):
            G.fromroot = sys.argv[1]
        else:
            print('ERROR: not a dir '+sys.argv[1])
            sys.exit(1)

    for dirName, subdirList, fileList in os.walk(G.fromroot):
        for fileBaseName in fileList:
            m = re.search(r'\.jpg$|\.jpeg$', fileBaseName, re.IGNORECASE)
            if m:
                filename = dirName+'/'+fileBaseName
                print(filename)
                doit(filename)

def doit(filename):
    if not os.path.isfile(filename):
        sys.exit(1)
    size = os.path.getsize(filename)
    # if size > 10*1024*1024:
    #     return

    extn = ''
    m = re.search(r'\.([^\.]+)$', filename)
    if m:
        extn = m.group(1)

    with open(filename, 'rb') as f:

        try:
            i = Image(f)
        except:
            print(f'NO EXIF: {filename}')
            return

        keys = set(dir(i))
        if 'datetime_original' in keys:
            dt = i.datetime_original
            # 2015:11:27 15:21:37
        elif 'datetime_digitized' in keys:
            dt = i.datetime_digitized
        elif 'datetime' in keys:
            dt = i.datetime
        else:
            print(f'NODATE: {filename}')
            print(dir(i))
            # TODO need to fix
            sys.exit(1)
            return
      
        m = re.search(r'^(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)$', dt)
        if m:
            (Y,M,D, h,m,s) = m.groups()
        else:
            print(f'NO-GOOD-DATE: {filename}')
            return
      
        dest_dirname  = f'{G.toroot}/{Y}/{Y}-{M}-{D}'
        dest_basename = f'{Y}{M}{D}-{h}{m}{s}-size-{size}.{extn}'
        dest = f'{dest_dirname}/{dest_basename}'
        if os.path.isfile(dest):
            import hashlib
            hash_dest = hashlib.md5(open(dest,'rb').read()).hexdigest()
            hash_new  = hashlib.md5(open(filename,'rb').read()).hexdigest()
            if hash_dest == hash_new:
                print(f'DUPE {dest} : {filename}')
                os.unlink(filename)
            else:
                print(f'DUPE-NOT {dest} : {filename}')

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
