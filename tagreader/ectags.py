#!/usr/bin/env python3
import json
import taglib
import subprocess
import io
from urllib.parse import quote
from codecs import decode

def convertpath(row):
    diskpath = row.strip('\n')
    tokenize = diskpath.split('/')
    tokenize.remove('')
    tokenize[0] = 'alexandria.wuvt.vt.edu'
    webpath = 'http://' + quote('/'.join(tokenize))
    return webpath


if __name__ == "__main__":
    data = []
    for path in ["/tank/automation", "/tank/library"]:
        findrun = subprocess.run(["find", path, "-type", "f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #findrun = subprocess.run(["find", path, "-type", "f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # need text=True on py38
        output = io.BytesIO(findrun.stdout)
        for rowbyte in output:
            try:
                row = decode(rowbyte)
            except:
                continue
            try:
                if row.endswith('flac\n'):
                    meta = taglib.File(row.strip('\n')).tags
                    try:
                        #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['LABEL'])
                        data.append({'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['LABEL'][0], 'file': convertpath(row) })
                    except KeyError:
                        continue
                    except IndexError:
                        continue
                elif row.endswith('mp3\n'):
                    meta = taglib.File(row.strip('\n')).tags
                    try:
                        #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['LABEL'])
                        data.append({'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['LABEL'][0], 'file': convertpath(row) })
                    except KeyError:
                            try:
                                #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['COMMENT'])
                                data.append({'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['COMMENT'][0], 'file': convertpath(row) })
                            except KeyError:
                                continue
                            except IndexError:
                                continue
                    except IndexError:
                            try:
                                #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['COMMENT'])
                                data.append({'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['COMMENT'][0], 'file': convertpath(row) })
                            except KeyError:
                                continue
                            except IndexError:
                                continue
            #occasionally we can't read a file for some reason. just skip
            except OSError:
                continue
    print(json.dumps(data))
