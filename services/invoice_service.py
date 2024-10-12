import datetime
from io import BytesIO
from typing import Optional

from loguru import logger
from sqlalchemy import desc

from app import db
from forms.invoice_form import InvoiceForm
from models.invoice import Invoice
from utils.invoice_pdf_util import create


def get_form(invoice: Optional[Invoice] = None) -> InvoiceForm:
    invoice_form = InvoiceForm()
    if invoice:
        invoice_form.set_data_from_model(invoice)
    return invoice_form


def get(invoice_id: int) -> Optional[Invoice]:
    invoice = db.session.get(Invoice, invoice_id)
    return invoice


def get_all() -> list[Invoice]:
    invoices = db.session.query(Invoice).order_by(Invoice.date_issued).all()
    return invoices


def get_filtered(
    client_id: Optional[int], date_min: Optional[str], date_max: Optional[str]
) -> list[Invoice]:
    query = db.session.query(Invoice)
    if client_id:
        logger.debug(f"{client_id = }")
        query = query.filter_by(client_id=client_id)
    if date_min:
        logger.debug(f"{date_min = }")
        query = query.filter(Invoice.date_issued >= date_min)
    if date_max:
        logger.debug(f"{date_max = }")
        query = query.filter(Invoice.date_issued <= date_max)
    invoices = query.order_by(Invoice.date_issued).all()
    return invoices


def update(invoice_id: int, invoice_data: dict) -> Optional[Invoice]:
    invoice = get(invoice_id=invoice_id)
    if invoice:
        invoice.update(invoice_data)
    return invoice


def delete(invoice_id: int):
    invoice = get(invoice_id=invoice_id)
    if invoice:
        invoice.delete()


def download(invoice_id: int):
    logger.debug(f"{invoice_id = }")
    invoice = get(invoice_id=invoice_id)
    if invoice:
        invoice.client_name = invoice.client.name
        invoice_pdf = create(invoice)
        download_name = f"{invoice.reference} (Invoice).pdf"
        pdf_file = BytesIO()
        pdf_file.write(invoice_pdf)
        pdf_file.seek(0)
        return pdf_file, download_name


def add(invoice_data: dict) -> Optional[Invoice]:
    invoice = Invoice.add(data=invoice_data)
    return invoice
