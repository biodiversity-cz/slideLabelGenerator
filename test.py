from slide_label_generator.process_file import process_uploaded_file


input_path = "test/template.xlsx"
output_path = "test/output.pdf"

process_uploaded_file(input_path, output_path, margin_top=2, margin_bottom=10,
              margin_left=5, margin_right=5, space_x=1, space_y=1)
