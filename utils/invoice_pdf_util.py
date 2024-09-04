from PIL import Image
from qrcodekit import qrcodekit
from models.invoice import Invoice
from utils.pdf_util import PDF


class InvoicePDF(PDF):
    def header(self, invoice: Invoice):
        super().header()

        self._y += 150  # in-line with header logo
        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._x = self._x_middle
        self._canvas.drawRightString(
            self._width - self._x_margin,
            self._y,
            f"Agreement For:",
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
            self._width - self._x_margin, self._y, invoice.client_name
        )
        self.line_break()

        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, f"Reference #:"
        )
        self.line_break()
        self.regular_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, invoice.reference
        )
        self.line_break()

        self.bold_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin, self._y, f"Date Issued:"
        )
        self.line_break()
        self.regular_font()
        self._x = self._x_margin + ((self._width - (2 * self._x_margin)) / 2)
        self._canvas.drawRightString(
            self._width - self._x_margin,
            self._y,
            invoice.date_issued.strftime("%B %d, %Y"),
        )

        self.line_break()
        self.line_break()
        self.line_break()
        self.line_break()


def create(invoice: Invoice):
    pdf = InvoicePDF()

    pdf.header(invoice)

    pdf.section("Project Details")

    pdf.subsection("Title")
    pdf._canvas.drawString(pdf._x, pdf._y, invoice.title)
    pdf.line_break()
    pdf.line_break()

    pdf.subsection("Summary")
    pdf.draw_text(invoice.summary)
    pdf.line_break()

    pdf.subsection("Technology")
    pdf.draw_text(invoice.technology)
    pdf.line_break()

    pdf.subsection("Duration")
    pdf.draw_text(invoice.estimated_duration)
    pdf.line_break()

    pdf.subsection("Cost")
    pdf.draw_text(invoice.estimated_cost)
    pdf.line_break()

    pdf.section("Success Criteria")
    pdf.draw_text(
        "All code functions in accordance to the details outlined above. Bug fixes are solved when discovered."
    )
    pdf.line_break()

    pdf.section("Payment")
    pdf.draw_text("All payments should be made to the following on-chain address:")
    pdf.line_break()
    # image = qrcodekit.get_image_with_data(invoice.payment_address)
    bitcoin_logo = Image.open("static/img/logo-bitcoin.png")
    bitcoin_logo = bitcoin_logo.convert("RGBA")
    image = qrcodekit.get_image_with_data_and_logo(
        invoice.payment_address, bitcoin_logo
    )
    pdf._x = pdf._x_middle - 150 / 2
    pdf.add_image(image, width=150, height=150)
    pdf.line_break()
    pdf.draw_text(invoice.payment_address, align="center")

    # TODO (ajrl) Add lightning invoice URL here: i.e.,
    # ajrlewis.com/pay?amount=<invoice.estimated_cost>&unit="btc"&memo=invoice.reference
    pdf.line_break()
    pdf.line_break()

    # Payment on a Bitcoin standard is easy, native to the internet and quick.
    # -> A unique on-chain payment address will be assigned to you.
    # -> A lightning invoice for the quote invoice
    # -> A payment for the exact amount to pay@ajrlewis.com
    # pdf.draw_text(
    #     "Alternatively, payments can be made to (1) a lightning invoice (generated here), or (2) the lightning address pay@ajrlewis.com."
    # )
    # pdf.line_break()
    # pdf.line_break()

    pdf.section("Terms & Conditions")

    pdf.subsection("Confidentiality")
    # "All concepts for this project are the property of the client. A.J.R. Lewis will maintain confidentiality and not disclose any proprietary information. Replica- tion of client data or ideas without permission is strictly prohibited."
    pdf.draw_text(
        """
All concepts for this project are the property of the client.
A.J.R. Lewis will maintain confidentiality and not disclose any proprietary information.
Replication of client data or ideas without permission is strictly prohibited.
"""
    )
    pdf.line_break()

    pdf.subsection("Payment Terms")
    # "A.J.R. Lewis and the client agree to a 50% downpayment of the quoted amount at the start of their collaboration. The remainder will be paid at the time of delivery of the agreed work. Both parties agree that an on-chain transaction to the above address with 3 confirmations constitutes as payment received by A.J.R. Lewis. It is the responsibility of A.J.R. Lewis to ensure correct payment details are sent to the client."
    #     pdf.draw_text(
    #         """
    # A.J.R. Lewis and the client agree to a 50% downpayment of the quoted amount at the start of their collaboration.
    # The remainder will be paid at the time of delivery of the agreed work.
    # Both parties agree that an on-chain transaction to the above address with 3 confirmations constitutes as payment received by A.J.R. Lewis.
    # It is the responsibility of A.J.R. Lewis to ensure correct payment details are sent to the client.
    #     """
    #     )
    pdf.draw_text(
        """
Full payment should be made by or on the first Sunday once this invoice is generated.
Both parties agree that an on-chain transaction to the above address for at least the required amount with 3 confirmations constitutes as payment received by A.J.R. Lewis.
It is the responsibility of A.J.R. Lewis to ensure correct payment details are sent to the client.
        """
    )
    pdf.line_break()

    pdf.subsection("Ownership Rights")
    # "A.J.R. Lewis retains ownership of any software created for the client until full payment is made. Upon full payment for the completed work, A.J.R. Lewis agrees to transfer to the client the copyright of the aforementioned work, in- cluding but not limited to all rights of reproduction, distribution, public perfor- mance, and adaptation, in all fields of exploitation, both currently known and hereafter devised. This transfer is triggered by the receipt of the full payment by A.J.R. Lewis (as defined above) and should take place immediately there- after. A.J.R. Lewis shall execute all documents and take all actions necessary to effectuate such copyright transfer to the client, ensuring the client acquires full and exclusive rights to the work for its entire duration of copyright under the law."
    pdf.draw_text(
        """
A.J.R. Lewis retains ownership of any software created for the client until full payment is made.
Upon full payment for the completed work, A.J.R. Lewis agrees to transfer to the client the copyright of the aforementioned work, including but not limited to all rights of reproduction, distribution, public performance, and adaptation, in all fields of exploitation, both currently known and hereafter devised.
This transfer is triggered by the receipt of the full payment by A.J.R. Lewis (as defined above) and should take place immediately thereafter.
A.J.R. Lewis shall execute all documents and take all actions necessary to effectuate such copyright transfer to the client, ensuring the client acquires full and exclusive rights to the work for its entire duration of copyright under the law.
"""
    )
    pdf.line_break()

    # pdf.section("Signature")
    # pdf.line_break()
    # pdf.line_break()
    # pdf.line_break()
    # pdf.line_break()
    # pdf.line_break()
    # pdf.draw_text("...............................")
    # pdf.draw_text("Signature of the client")
    # pdf.line_break()
    # pdf.line_break()
    # pdf.line_break()
    # pdf.line_break()
    # pdf.line_break()
    # pdf.draw_text("...............................")
    # pdf.draw_text("Date")

    pdf.save()

    return pdf.to_bytes()
