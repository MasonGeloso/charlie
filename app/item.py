from datetime import datetime
from secrets import token_hex

from .globals import ITEM_TABLE
from .globals import ITEMS



class Item(object):
    def __init__(self, invoice_date=None, shipment_date=None, GUI=None,
                 description = None, catalog=None, invoice=None, status='UNSCANNED',
                 lot_id=None, catalog_lot=None, serial=None, identifier=None, source='RGA',
                 rga=None, purchase_order=None, filename=None):

        self.invoice_date = invoice_date
        self.shipment_date = shipment_date
        self.GUI = GUI
        self.status = status
        self.description = description
        self.catalog = catalog
        self.invoice = invoice
        self.source = source
        self.filename = filename
        self.purchase_order = purchase_order
        self.lot_id = lot_id
        self.catalog_lot = catalog_lot
        self.serial = serial
        self.rga = rga
        self.history = []
        self.table = 'IncomingItem'
        ITEMS.append(self)

        if not identifier:
            self.identifier = token_hex(8)
            self.write()
        else:
            self.identifier = identifier
            self.save()


    def to_dict(self):
        return {
            'invoice_date': self.invoice_date,
            'shipment_date': self.shipment_date,
            'GUI': self.GUI,
            'description': self.description,
            'catalog': self.catalog,
            'invoice': self.invoice,
            'status': self.status,
            'lot_id': self.lot_id,
            'catalog_lot': self.catalog_lot,
            'serial': self.serial,
            'identifier': self.identifier
        }



    def save(self):
        
        ITEM_TABLE.insert(
            self.to_dict()
        )


    def write(self):
        pass


    def __repr__(self):
        return f'<Item: {self.catalog}, {self.description}, {self.source}, {self.filename}>'



def load_items():
    pass

def get_item(value, by='serial'):

    for i in ITEMS:
        if getattr(i, by) == value:
            return i


def get_non_serial_item(lot_id, catalog, create_overflow_item=True, user=None):

    for item in ITEMS:
        if item.serial:
            continue

        if item.lot_id == lot_id and item.catalog == catalog and item.source == 'RGA':
            return item

    if create_overflow_item:
        new_item = Item(lot_id=lot_id, catalog=catalog, source='Overflow',
                        filename='SCANNED IN', status='SCANNED')
        new_item.history.append({
            'datetime': datetime.now().strftime('%m/%d/%y %H:%M'),
            'user': user,
            'text': f'Item has been scanned into overflow by {user}'
        })
        return new_item


def set_item_attr(item, key, value, user=None):

    old_value = getattr(item, key)

    setattr(item, key, value)

    item.history.append({
        'datetime': datetime.now().strftime('%m/%d/%y %H:%M'),
        'user': user,
        'key': key,
        'new_value': value,
        'old_value': old_value,
        'text': (f'The {key} was changed from {old_value} to '
                 f'{value} by {user if user else "a not logged in user"}')
    })


def get_count():

    types = {}

    for i in ITEMS:
        if not i.source in types.keys():
            types[i.source] = 1
        else:
            types[i.source] += 1

    return types