import pandas as pd
from slide_label_generator.workers.writer_pdf import write_pdf
from slide_label_generator.workers.excel_reader import read_table


def process_uploaded_file(input_path, output_path):
    data = read_table(input_path)

    write_pdf(data, output_path, margin_top=2, margin_bottom=20,
              margin_left=15, margin_right=15)
