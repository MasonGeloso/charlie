from os import path
from secrets import token_hex
from traceback import format_exc

from flask import Flask
from flask import send_file
from flask import redirect
from flask import render_template
from flask import request

from .barcode import parse
from .globals import ITEMS
from .item import get_count
from .item import get_non_serial_item
from .item import get_item
from .item import Item
from .item import set_item_attr
from .xlsx_utils import sterilize_excel_date
from .xlsx_utils import read_xlsx


app = Flask(__name__)


@app.route('/items')
def items_endpoint():
    return render_template('items.html', items=ITEMS, count=get_count())

@app.route('/')
@app.route('/set_user_name')
def set_user_name():
    return render_template('set_user_name.html')

@app.route('/reports')
def reports():

    from .reports import generate_report

    if request.args.get('master_report') == 'true':
        filename = generate_report('master_report')
        return send_file(
            path.join('reports', filename),
            attachment_filename=filename)

    if request.args.get('approved_report') == 'true':
        filename = generate_report('approved_report')
        return send_file(
            path.join('reports', filename),
            attachment_filename=filename)

    if request.args.get('declined_report') == 'true':
        filename = generate_report('declined_report')
        return send_file(
            path.join('reports', filename),
            attachment_filename=filename)

    return render_template('reports.html')


@app.route('/scanner', methods=['PUT', 'GET'])
def scanner():
    if request.method == 'GET':
        return render_template('scanner.html')

    if request.method == 'PUT':

        data = request.get_json()

        barcode_data = parse(data.get('barcode'))
        status = data.get('status')
        user = request.args.get('user')
        dup_override = True if request.args.get('dupOverride') == 'true' else False

        # Data is incomplete
        if not barcode_data or not status:
            return f'No barcode data or status provided! => {data}', 500

        # Check for duplicates by serial
        possible_dup = get_item(barcode_data.get('serial'))

        if possible_dup and dup_override != True:
            return f'Duplicate detected: {barcode_data.get("serial")}', 400

        # Check if items remaining
        i = get_non_serial_item(
            barcode_data.get('lot_id'),
            barcode_data.get('catalog'),
            user=user, dup_override=dup_override
        )

        # Set attribute
        set_item_attr(i, 'serial', barcode_data.get('serial'), user=user)
        set_item_attr(i, 'status', status, user=user)

        return {'barcode': barcode_data, 'status': status}, 200



@app.route('/upload_rga', methods=['POST', 'GET'])
def upload_rga():
    if request.method == 'GET':
        return render_template('importExcel.html', title='Upload RGA Excel')

    if request.method == 'POST':

        try:

            # Create filename
            filename = path.join(
                app.root_path, 'PackingListData', f'{token_hex(8)}.xlsx')
            real_filename = request.files['file'].filename

            # Save Image
            request.files['file'].save(
                filename
            )

            # Parse XLSX data
            items = read_xlsx(filename)

            {
                'RGA#': 'CMS0008-RGA01',
                'Medtronic Purchase Order#': 'PO153099',
                'SKU Code': 'WAIN-CKI-10-200',
                'Item Description': 'CHIKAI 10 Neurovascular Guide Wire .010 200cm',
                'Lot ID': '200804A02A', 
                'Approved Quantity': 4.0
            }


            # Create each item
            for itemCatagory in items:
                for item in range(int(itemCatagory['Approved Quantity'])):
                    Item(**{
                        'rga': itemCatagory.get('RGA#'),
                        'purchase_order': itemCatagory.get('Medtronic Purchase Order#'),
                        'catalog': itemCatagory.get('SKU Code'),
                        'lot_id': itemCatagory.get('Lot ID'),
                        'description': itemCatagory.get('Item Description'),
                        'source': 'RGA',
                        'filename': real_filename
                    })


            return redirect('/items')

        except:
            return {
                'status': 'failure',
                'data': format_exc()
            }



@app.route('/upload_packing_list', methods=['GET', 'POST'])
def upload_packing_list():
    if request.method == 'GET':
        return render_template(
            'importExcel.html', title='Upload Packing List Excel')

    if request.method == 'POST':

        try:

            # Create filename
            filename = path.join(
                app.root_path, 'PackingListData', f'{token_hex(8)}.xlsx')
            real_filename = request.files['file'].filename

            # Save Image
            request.files['file'].save(
                filename
            )

            # Parse XLSX data
            items = read_xlsx(filename)

            {
                'RGA#': 'CMS0008-RGA01',
                'Medtronic Purchase Order#': 'PO153099',
                'SKU Code': 'WAIN-CKI-10-200',
                'Item Description': 'CHIKAI 10 Neurovascular Guide Wire .010 200cm',
                'Lot ID': '200804A02A', 
                'Approved Quantity': 4.0
            }


            # Create each item
            for itemCatagory in items:
                for item in range(int(itemCatagory['Approved Quantity'])):
                    Item(**{
                        'rga': itemCatagory.get('RGA#'),
                        'purchase_order': itemCatagory.get('Medtronic Purchase Order#'),
                        'catalog': itemCatagory.get('SKU Code'),
                        'lot_id': itemCatagory.get('Lot ID'),
                        'description': itemCatagory.get('Item Description'),
                        'source': 'Packing List',
                        'filename': real_filename
                    })


            return redirect('/items')

        except:
            return {
                'status': 'failure',
                'data': format_exc()
            }