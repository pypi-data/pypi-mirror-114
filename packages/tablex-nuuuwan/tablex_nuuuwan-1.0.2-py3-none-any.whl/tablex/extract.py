import csv
import re

import camelot
from dateutil.parser import parse
from dateutil.parser._parser import ParserError

REGEX_INT = r'^\d+$'


def parse_date(cleaned_cell):
    try:
        if len(cleaned_cell) > 10:
            cleaned_cell = cleaned_cell[:10]
        return parse(cleaned_cell, fuzzy=True)
    except ParserError:
        return None


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
    )
    tables[0].to_csv(csv_file)


def csv_to_cleaned_tsv(csv_file, tsv_file):
    cleaned_rows = []
    with open(csv_file) as fin:
        csv_reader = csv.reader(fin, delimiter=',')
        for row in csv_reader:
            cleaned_row = []
            for cell in row:
                cleaned_cell = get_cleaned_cell(cell)
                cleaned_row.append(cleaned_cell)
            cleaned_rows.append(cleaned_row)

    with open(tsv_file, mode='w') as fout:
        csv_writer = csv.writer(fout, delimiter='\t')

        for cleaned_row in cleaned_rows:
            csv_writer.writerow(cleaned_row)


if __name__ == '__main__':
    pdf_file = 'src/tablex/tests/test.epid.2021-07-29.pdf'
    csv_file = '/tmp/test.tablex.test.csv'
    pdf_to_csv(pdf_file, csv_file)

    tsv_file = '/tmp/test.tablex.test.tsv'
    csv_to_cleaned_tsv(csv_file, tsv_file)
    import os

    os.system('open %s' % tsv_file)
