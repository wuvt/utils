#!/usr/bin/env python3
import sys
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
    modifile = sys.argv[1]
    data = json.load(open(modifile))
    for path in ["/tank/automation", "/tank/library"]:
        findrun = subprocess.run(["find", path, "-type", "f", "-newer", modifile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = io.BytesIO(findrun.stdout)
        for rowbyte in output:
            try:
                row = decode(rowbyte)
            except:
                continue
            try:
                if row.endswith('flac\n') or row.endswith('ogg\n'):
                    f = taglib.File(row.strip('\n'))
                    meta = f.tags
                    try:
                        #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['LABEL'])
                        ndata = {'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['LABEL'][0], 'url': convertpath(row) }
                        ndata['length'] = f.length
                        ndata['bitrate'] = f.bitrate
                        ndata['sample'] = f.sampleRate
                        data.append(ndata)
                    except KeyError:
                        continue
                    except IndexError:
                        continue
                elif row.endswith('mp3\n') or row.endswith('MP3\n'):
                    f = taglib.File(row.strip('\n'))
                    meta = f.tags
                    try:
                        #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['LABEL'])
                        ndata = {'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['LABEL'][0], 'url': convertpath(row) }
                        ndata['length'] = f.length
                        ndata['bitrate'] = f.bitrate
                        ndata['sample'] = f.sampleRate
                        data.append(ndata)
                    except KeyError:
                            try:
                                #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['COMMENT'])
                                ndata = {'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['COMMENT'][0], 'url': convertpath(row) }
                                ndata['length'] = f.length
                                ndata['bitrate'] = f.bitrate
                                ndata['sample'] = f.sampleRate
                                data.append(ndata)
                            except KeyError:
                                continue
                            except IndexError:
                                continue
                    except IndexError:
                            try:
                                #print(meta['TITLE'], meta['ARTIST'], meta['ALBUM'], meta['COMMENT'])
                                data.append({'title': meta['TITLE'][0], 'artist': meta['ARTIST'][0], 'album': meta['ALBUM'][0], 'label': meta['COMMENT'][0], 'url': convertpath(row) })
                            except KeyError:
                                continue
                            except IndexError:
                                continue
            #occasionally we can't read a file for some reason. just skip
            except OSError:
                continue
    print(json.dumps(data))
