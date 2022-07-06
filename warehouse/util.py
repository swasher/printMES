import os
import fnmatch
from smb.SMBConnection import SMBConnection

def smbwalk(conn, shareddevice, top=u'/', pattern='*'):
    """
    smbwalk recursively search for files matching `pattern` on `shareddevice/top` samba path.
    Return list of tuple like (path to file, smb.base.SharedFile instances).
    
    Note, we can't use pattern filtering via conn.listPath(shareddevice, top, pattern=pattern) becouse
    it's do not return subdir (subdir not match to pattern). So we manually matching to pattern inside cycle.
    """
    dirs, nondirs = [], []

    if not isinstance(conn, SMBConnection):
        raise TypeError("SMBConnection required")

    names = conn.listPath(shareddevice, top)

    for name in names:
        if name.isDirectory:
            if name.filename not in [u'.', u'..']:
                dirs.append(name.filename)
        else:
            if fnmatch.fnmatch(name.filename, pattern):
                #nondirs.append(name.filename)
                nondirs.append(name)

    #yield top, dirs, nondirs
    if nondirs:
        for f in nondirs:
            yield (top, f)

    for name in dirs:
        new_path = os.path.join(top, name)
        for x in smbwalk(conn, shareddevice, new_path, pattern=pattern):
            yield x