from io import BytesIO
import sys
import time

import bitcoinkit.utils as bitcoinkit_utils
from bitcoinkit.vendor.mempool import address, price
from flask import current_app as app
from loguru import logger
import pandas as pd

sys.path.append("./")
from app import create_app, db
from configs.prod_config import ProdConfig
from models import Invoice, Receipt
from utils import receipt_pdf_util

app = create_app(ProdConfig)


def create(invoice_id: int, currency: str):
    # Get the invoice
    invoice = db.session.query(Invoice).filter_by(invoice_id=invoice_id).first()
    logger.debug(f"{invoice = }")

    # Get parameters needed to find correct transaction
    value = invoice.value
    timestamp = invoice.date_issued
    bitcoin_address = invoice.payment_address
    logger.debug(f"{value = }")
    logger.debug(f"{timestamp = }")
    logger.debug(f"{bitcoin_address = }")

    # Get transaction associated to the address
    transactions = address.transaction_details(bitcoin_address)
    logger.debug(f"{transactions = }")
    df = pd.DataFrame(transactions)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    mask = (df["value"] == value) & (df["timestamp"] >= timestamp)
    df = df.loc[mask]
    timestamp = f"{timestamp}"
    transaction_id = df.iloc[0].txid
    block_height = df.iloc[0].block_height
    block_time = df.iloc[0].block_time
    logger.debug(f"{transactions = }")

    # Get the fiat value of the bitcoin at time of transaction
    price_currency = price.historical(timestamp, currency=currency)
    logger.debug(f"{price_currency = }")
    value_currency = bitcoinkit_utils.satoshis_to_bitcoins(value) * price_currency
    logger.debug(f"{value_currency = }")

    # Create and add receipt object
    data = {
        "invoice_id": invoice_id,
        "transaction_id": transaction_id,
        "timestamp": timestamp,
        "block_time": block_time,
        "block_height": block_height,
        "fiat": currency,
        "value_fiat": value_currency,
    }
    logger.debug(f"{data = }")
    receipt = Receipt.add(data)
    logger.debug(f"{receipt = }")
    return receipt


def create_pdf(receipt_id):
    receipt = db.session.query(Receipt).filter_by(receipt_id=receipt_id).first()
    invoice = receipt.invoice
    logger.debug(f"{receipt = }")
    logger.debug(f"{invoice = }")
    pdf = receipt_pdf_util.create(invoice, receipt)
    download_name = f"{invoice.reference} (Receipt).pdf"
    pdf_file = BytesIO()
    pdf_file.write(pdf)
    pdf_file.seek(0)
    return pdf_file, download_name


def main():
    with app.app_context():
        # for invoice_id in [1, 2, 3, 4, 5, 6]:
        #     currency = "GBP"
        #     receipt = create(invoice_id=invoice_id, currency=currency)
        #     logger.info(f"{receipt = }")
        #     time.sleep(0.5)

        for receipt_id in [1, 2, 3, 4, 5, 6]:
            pdf_file, download_name = create_pdf(receipt_id=receipt_id)
            with open(download_name, "wb") as f:
                f.write(pdf_file.getbuffer())


if __name__ == "__main__":
    main()
