from stardb.storage import BlockFile
from stardb.databases import AssetDatabase

from hashlib import sha256

if __name__ == '__main__':
    bf = BlockFile('C:\\SSDSteam\\SteamApps\\common\\Starbound\\assets\\packed.pak')
    db = AssetDatabase(bf)
    db.open()
    #print(db.getFileList())
    #print(db['/weather/snow/snow.weather'])

    #db['/animations/muzzleflash/bulletmuzzle1/bulletmuzzle1.frames']
    #print(db['/animations/muzzleflash/bulletmuzzle1/bulletmuzzle1.png'])
    """
    total = 0
    fail = 0
    for name in db.getFileList():
        try:
            db[name]
        except KeyError:
            print(name)
            fail += 1
        total += 1
    print(total, fail)
    """

    print(db.getBrokenFiles())
