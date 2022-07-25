from pathlib import Path

from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
from decimal import Decimal

from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable

from .models import PrintSheet

class PrintOrder(object):
    def __init__(self, order):

        # create an empty Document
        self.pdf = Document()

        # add an empty Page
        page = Page()
        self.pdf.add_page(page)

        # use a PageLayout (SingleColumnLayout in this case)
        layout: PageLayout = SingleColumnLayout(page)

        # add a Paragraph object
        layout.add(Paragraph(f"Order #{order.order}", font_size=18))

        lists = PrintSheet.objects.filter(order__pk=order.pk)
        if lists:
            table = FixedColumnWidthTable(number_of_columns=3, number_of_rows=len(lists))

            for l in lists:
                table.add(Paragraph(l.name))
                table.add(Paragraph(l.description))
                table.add(Paragraph(l.printingpress.name))

            table.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
            layout.add(table)


    def printpdf(self):
        # store the PDF
        with open(Path("output.pdf"), "wb") as pdf_file_handle:
            PDF.dumps(pdf_file_handle, self.pdf)

