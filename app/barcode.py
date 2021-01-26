


def parse(barcode):
    """Parses barcode and returns dict of data

    Args:
        barcode (str): The item barcode
    """

    if barcode.find('(D@02)') == -1:
        return

    serial = barcode[barcode.find('(D@02)')+6:barcode.find('(D@03)')]

    GUI = barcode[barcode.find('(D@14)')+6:]
    if GUI[-2:] == r'\n':
        GUI = GUI[:-2]

    lot_id = barcode[barcode.find('(D@04)')+6:barcode.find('(D@05)')]

    Exp_Date = barcode[barcode.find('(D@08)')+6:barcode.find('(D@09)')]

    catalog = barcode[barcode.find('(D@11)')+6:barcode.find('(D@12)')]

    catalog = catalog[:catalog.find(' ')]


    return {
        'GUI': GUI,
        'lot_id': lot_id,
        'catalog': catalog,
        'serial': serial
    }
