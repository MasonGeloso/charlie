from datetime import datetime
from xlrd import open_workbook



def read_xlsx(xlsx_file, sheet_index=0):
    """Reads in an excel file and returns list of objects

    Args:
        xlsx_file (str): path to xlsx file
    """

    dict_list = list()
    wb = open_workbook(xlsx_file)

    sheet = wb.sheet_by_index(sheet_index)

    # read first row for keys  
    keys = sheet.row_values(0)

    # read the rest rows for values
    values = [sheet.row_values(i) for i in range(1, sheet.nrows)]

    for value in values:
        dict_list.append(dict(zip(keys, value)))

    return dict_list



def sterilize_excel_date(date):
    return datetime.fromordinal(
        datetime(1900, 1, 1).toordinal() + int(date) - 2).strftime('%m/%d/%Y')


if __name__ == '__main__':
    print(
        read_xlsx(r"C:\Users\mason\Desktop\210111 RGA Request.xlsx", sheet_index=2)
    )

