from bitcoinkit import utils as bitcoinkit_utils
from PIL import Image
from qrcodekit import qrcodekit

from models import Invoice, Receipt
from utils.pdf_util import PDF


class ReceiptPDF(PDF):
    def header(self, invoice: Invoice, receipt: Receipt):
        super().header()

        self._y += 150  # in-line with header logo
        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._x = self._x_middle
        self._canvas.drawRightString(
            self._width - self._x_margin,
            self._y,
            f"Receipt For:",
        )
        self.line_break()

        self.regular_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin,
            self._y,
            f"Tech Solutions Consultancy & Services",
        )
        self.line_break()

        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(self._width - self._x_margin, self._y, f"Client:")
        self.line_break()
        self.regular_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, invoice.client.name
        )
        self.line_break()

        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, f"Invoice Reference #:"
        )
        self.line_break()
        self.regular_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, invoice.reference
        )
        self.line_break()

        # self.bold_font()
        # self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        # self._canvas.drawRightString(
        #     self._width - self._x_margin, self._y, f"Date Issued:"
        # )
        # self.line_break()
        # self.regular_font()
        # self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        # self._canvas.drawRightString(
        #     self._width - self._x_margin,
        #     self._y,
        #     invoice.date_issued.strftime("%B %d, %Y"),
        # )
        # self.line_break()

        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, f"Date Paid:"
        )
        self.line_break()
        self.regular_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin,
            self._y,
            receipt.timestamp.strftime("%B %d, %Y"),
        )

        self.line_break()
        self.line_break()
        self.line_break()
        self.line_break()
        self.line_break()
        self.line_break()


def create(invoice: Invoice, receipt: Receipt):
    pdf = ReceiptPDF()

    pdf.header(invoice, receipt)

    pdf.section("Transaction Details")

    pdf.subsection("ID")
    pdf._canvas.drawString(pdf._x, pdf._y, receipt.transaction_id)
    pdf.line_break()
    pdf.line_break()

    pdf.subsection("Block Height")
    pdf._canvas.drawString(pdf._x, pdf._y, f"{receipt.block_height}")
    pdf.line_break()
    pdf.line_break()

    pdf.subsection("Block Time")
    pdf._canvas.drawString(pdf._x, pdf._y, f"{receipt.block_time}")
    pdf.line_break()
    pdf.line_break()

    pdf.subsection("Value")
    pdf.draw_text(
        f"{bitcoinkit_utils.to_string(invoice.value)} ({receipt.value_fiat:,.2f} {receipt.fiat.upper()})"
    )
    pdf.line_break()

    pdf.line_break()
    pdf.line_break()

    pdf.bold_font()
    pdf.draw_text("Thank you for your business!", align="center")
    pdf.regular_font()
    pdf.line_break()

    pdf.save()

    return pdf.to_bytes()
