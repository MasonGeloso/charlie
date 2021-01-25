from tinydb import TinyDB


LISTEN = True


DATABASE = TinyDB('data.json')
ITEMS = []
ITEM_TABLE = DATABASE.table('ItemTable')