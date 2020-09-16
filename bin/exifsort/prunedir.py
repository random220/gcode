import os,sys

class G:
    fromroot = '/shares/data/memories/Blackmachine-under-om-desk'
    toroot   = '/shares/data/memories/SORTED'

def main():

    todel = []
    for dirName, subdirList, fileList in os.walk(G.fromroot):
        if len(subdirList) == 0 and len(fileList) == 0:
            todel.append(dirName)

    for d in todel:
        os.rmdir(d)

main()
