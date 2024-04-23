from models.invoice import Invoice

# from utils import pdf_util


def create(invoice: Invoice) -> pdf_util.PDF:
    pdf = pdf_util.create(title="Invoice for Tech Solutions Consultancy & Services")
    # pdf.section("Project Details")
    # pdf.subsection("Title")
    # pdf.content(invoice.title)
    # pdf.subsection("Summary")
    # pdf.content(invoice.summary)
    return pdf.render()
