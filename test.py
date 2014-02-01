from stardb.storage import BlockFile
from stardb.databases import SimpleSha256Database

if __name__ == '__main__':
    f = open('C:\\SSDSteam\\SteamApps\\common\\Starbound\\assets\\packed.pak', 'rb')

    bf = BlockFile(f)
    db = SimpleSha256Database(bf, 'Assets1')
    db.open()
    print(bf.getDebugInfo())
    print(db.getDebugInfo())
    
    try:
        db['_index']
        print("Found")
    except KeyError:
        print("Not Found")

# AssetsDatabaseBackend
# _digest
# _index
