import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus.flowables import Flowable
from slide_label_generator.standard_print.label import Label


def write_pdf(data: pd.DataFrame, path: str, margin_top: float = 10,
              margin_bottom: float = 10, margin_left: float = 10,
              margin_right: float = 10, padding: float = 1,
              space_x: int = 1, space_y: int = 1) -> None:
    """
    Create a PDF with A4 paper size and configurable margins.
    
    Args:
        data: DataFrame containing the data to be written to PDF
        path: Output path for the PDF file
        margin_top: Top margin in mm (default: 10)
        margin_bottom: Bottom margin in mm (default: 10)
        margin_left: Left margin in mm (default: 10)
        margin_right: Right margin in mm (default: 10)
        padding: Internal padding for labels in mm (default: 1)
        space_x: Horizontal spacing between labels (default: 1)
        space_y: Vertical spacing between labels (default: 1)
    """
    # Create document with A4 size and specified margins
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        topMargin=margin_top * mm,
        bottomMargin=margin_bottom * mm,
        leftMargin=margin_left * mm,
        rightMargin=margin_right * mm
    )

    # Define label size
    label_width = 24 * mm
    label_height = 24 * mm

    # Calculate available space for labels
    available_width = A4[0] - (margin_left + margin_right) * mm
    available_height = A4[1] - (margin_top + margin_bottom) * mm

    # Calculate number of labels that fit in each row and column
    labels_per_row = int(available_width // ((label_width + space_x * mm) +  space_x * mm))
    labels_per_column = int(available_height // ((label_height + space_y * mm) + space_y * mm))

    # Create labels from DataFrame (excluding header)
    labels = [Label(row, label_width, label_height, padding * mm) for _, row in data.iterrows()]

    # Arrange labels in a grid
    elements = []

    # Create pages of labels
    page_label_count = labels_per_row * labels_per_column
    for page_start in range(0, len(labels), page_label_count):
        # Add page break before each page except the first
        if page_start > 0:
            from reportlab.platypus import PageBreak
            elements.append(PageBreak())

        # Get labels for this page
        page_labels = labels[page_start:page_start + page_label_count]

        # Create a grid (list of lists) for this page
        grid_data = []
        for row_idx in range(labels_per_column):
            row_data = []
            for col_idx in range(labels_per_row):
                label_idx = row_idx * labels_per_row + col_idx
                if label_idx < len(page_labels):
                    row_data.append(page_labels[label_idx])
                else:
                    # Add empty cell if no label
                    row_data.append("")
            grid_data.append(row_data)

        # Create table with labels
        table = Table(grid_data, colWidths=label_width + space_x * mm, rowHeights=label_height + space_y * mm)

        # Add table to elements
        elements.append(table)

    # Build PDF
    doc.build(elements)
