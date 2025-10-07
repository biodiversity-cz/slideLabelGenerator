import pandas as pd
from slide_label_generator.workers.writer_pdf import write_pdf
from slide_label_generator.workers.excel_reader import read_table


def process_uploaded_file(input_path, output_path, margin_top=10, margin_bottom=10,
              margin_left=5, margin_right=5, space_x=1, space_y=1):
    data = read_table(input_path)

    write_pdf(data, output_path, margin_top, margin_bottom,
              margin_left, margin_right, space_x, space_y)
