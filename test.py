from stardb.storage import BlockFile
from stardb.databases import AssetDatabase

if __name__ == '__main__':
    f = open('C:\\SSDSteam\\SteamApps\\common\\Starbound\\assets\\packed.pak', 'rb')

    bf = BlockFile(f)
    db = AssetDatabase(bf)
    db.open()
    print(db.getFileList())
    print(db['/weather/snow/snow.weather'])
