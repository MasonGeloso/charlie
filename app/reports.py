from copy import deepcopy
from secrets import token_hex
from os import path
from xlsxwriter import Workbook

from . import app
from .item import ITEMS


def generate_report(report):

    filename = f'{token_hex(8)}.xlsx'
    workbook = Workbook(path.join(app.root_path, 'reports', filename))
    bold = workbook.add_format({'bold': True, "shrink" : True})

    if report == 'master_report':
        worksheet = workbook.add_worksheet('All Items')

        # Write Headers
        worksheet.write(0, 0, 'Source', bold)
        worksheet.write(0, 1, 'Filename', bold)
        worksheet.write(0, 2, 'Serial', bold)
        worksheet.write(0, 3, 'Catalog', bold)
        worksheet.write(0, 4, 'Lot ID', bold)
        worksheet.write(0, 5, 'Description', bold)
        worksheet.write(0, 6, 'GUI', bold)
        worksheet.write(0, 7, 'Status', bold)
        worksheet.write(0, 8, 'Last Activity', bold)

        for row, item in enumerate(ITEMS):
            row += 1
            worksheet.write(row, 0, item.source)
            worksheet.write(row, 1, item.filename)
            worksheet.write(row, 2, item.serial)
            worksheet.write(row, 3, item.catalog)
            worksheet.write(row, 4, item.lot_id)
            worksheet.write(row, 5, item.description)
            worksheet.write(row, 6, item.GUI)
            worksheet.write(row, 7, item.status)
            worksheet.write(row, 8, str(item.history[-1].get('text')) if item.history else '')

    if report == 'approved_report':
        worksheet = workbook.add_worksheet('Approved Items')

        # Write Headers
        worksheet.write(0, 0, 'Source', bold)
        worksheet.write(0, 1, 'Filename', bold)
        worksheet.write(0, 2, 'Serial', bold)
        worksheet.write(0, 3, 'Catalog', bold)
        worksheet.write(0, 4, 'Lot ID', bold)
        worksheet.write(0, 5, 'Description', bold)
        worksheet.write(0, 6, 'GUI', bold)
        worksheet.write(0, 7, 'Status', bold)
        worksheet.write(0, 8, 'Last Activity', bold)

        for row, item in enumerate([i for i in ITEMS if i.status == 'Approved']):
            row += 1
            worksheet.write(row, 0, item.source)
            worksheet.write(row, 1, item.filename)
            worksheet.write(row, 2, item.serial)
            worksheet.write(row, 3, item.catalog)
            worksheet.write(row, 4, item.lot_id)
            worksheet.write(row, 5, item.description)
            worksheet.write(row, 6, item.GUI)
            worksheet.write(row, 7, item.status)
            worksheet.write(row, 8, str(item.history[-1].get('text')) if item.history else '')


    if report == 'declined_report':
        worksheet = workbook.add_worksheet('Declined Items')

        # Write Headers
        worksheet.write(0, 0, 'Source', bold)
        worksheet.write(0, 1, 'Filename', bold)
        worksheet.write(0, 2, 'Serial', bold)
        worksheet.write(0, 3, 'Catalog', bold)
        worksheet.write(0, 4, 'Lot ID', bold)
        worksheet.write(0, 5, 'Description', bold)
        worksheet.write(0, 6, 'GUI', bold)
        worksheet.write(0, 7, 'Status', bold)
        worksheet.write(0, 8, 'Last Activity', bold)

        for row, item in enumerate([i for i in ITEMS if i.status == 'Declined']):
            row += 1
            worksheet.write(row, 0, item.source)
            worksheet.write(row, 1, item.filename)
            worksheet.write(row, 2, item.serial)
            worksheet.write(row, 3, item.catalog)
            worksheet.write(row, 4, item.lot_id)
            worksheet.write(row, 5, item.description)
            worksheet.write(row, 6, item.GUI)
            worksheet.write(row, 7, item.status)
            worksheet.write(row, 8, str(item.history[-1].get('text')) if item.history else '')

    workbook.close()
    return filename