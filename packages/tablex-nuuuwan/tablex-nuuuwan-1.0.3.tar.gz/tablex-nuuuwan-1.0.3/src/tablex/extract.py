import csv
import datetime
import re

import camelot
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from utils import jsonx

from tablex._utils import log

REGEX_INT = r'^\d+$'


def parse_date(cleaned_cell):
    try:
        if len(cleaned_cell) > 10:
            cleaned_cell = cleaned_cell[:10]
        return parse(cleaned_cell, fuzzy=True)
    except ParserError:
        return None


def is_header_row(row):
    n_str = 0
    n_int = 0
    n_date = 0
    for cell in row:
        if isinstance(cell, str) and len(cell) > 0:
            n_str += 1
        if isinstance(cell, int):
            n_int += 1
        if isinstance(cell, datetime.datetime):
            n_date += 1
    return n_str > (n_int + n_date)


def is_null_row(row):
    for cell in row:
        if cell != '':
            return False
    return True


def get_cleaned_cell(cell):
    cleaned_cell = cell.replace('\n', ' ')
    cleaned_cell = re.sub(r'[^a-zA-Z0-9_\-.]+', '', cleaned_cell)
    cleaned_cell = cleaned_cell.replace('-V', '')
    if len(cleaned_cell) > 1 and cleaned_cell[0] == '-':
        cleaned_cell = cleaned_cell[1:]

    re_int = re.search(REGEX_INT, cleaned_cell)
    if re_int:
        return (int)(cleaned_cell)

    cleaned_cell_date = parse_date(cleaned_cell)
    if cleaned_cell_date is not None:
        return cleaned_cell_date

    if cleaned_cell == '-':
        return 0

    return cleaned_cell


def pdf_to_csv(pdf_file, csv_file):
    tables = camelot.read_pdf(
        pdf_file,
        line_scale=50,
        verbose=False,
    )
    tables[0].to_csv(csv_file)
    log.info('Converted %s and saved to %s', pdf_file, csv_file)


def csv_to_json(csv_file, json_file):
    cleaned_rows = []
    with open(csv_file) as fin:
        csv_reader = csv.reader(fin, delimiter=',')
        for row in csv_reader:
            cleaned_row = []
            for cell in row:
                cleaned_cell = get_cleaned_cell(cell)
                cleaned_row.append(cleaned_cell)
            cleaned_rows.append(cleaned_row)

    prev_data_row = False
    header_i_list = []
    data_list = []
    for i, row in enumerate(cleaned_rows):
        if is_null_row(row):
            continue
        if is_header_row(row):
            if not prev_data_row:
                header_i_list.append(i)
            else:
                header_i_list[-1] = i
                print(header_i_list)
        else:  # data row
            prev_data_row = True
            data = {}
            for j, cell in enumerate(row):
                if isinstance(cell, datetime.datetime):
                    cell = str(cell)
                elif cell == '':
                    cell = 0

                key_cell_list = []
                for i_key in header_i_list:
                    j_key = j
                    key_cell = ''
                    while key_cell == '':
                        key_cell = cleaned_rows[i_key][j_key]
                        j_key -= 1
                    key_cell_list.append(key_cell)
                key = '.'.join(key_cell_list)
                data[key] = cell

            data_list.append(data)
    jsonx.write(json_file, data_list)
    log.info(
        'Parsed %s and saved %d rows to to %s',
        csv_file,
        len(data_list),
        json_file,
    )


if __name__ == '__main__':
    date = '2021-01-29'
    pdf_file = 'src/tablex/tests/test.epid.%s.pdf' % (date)
    csv_file = '/tmp/test.tablex.%s.csv' % (date)
    pdf_to_csv(pdf_file, csv_file)

    json_file = '/tmp/test.tablex.%s.json' % (date)
    csv_to_json(csv_file, json_file)
    import os

    os.system('open %s' % json_file)
