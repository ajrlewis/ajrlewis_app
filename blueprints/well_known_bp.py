from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template

well_known_bp = Blueprint("well_known_bp", __name__)


@well_known_bp.route("/", methods=["GET"])
def get():
    return {"message": "Hello world!"}


# https://livingroomofsatoshi.com/api/v1/lnurl/payreq/5ae9f8da-7b0a-4f11-b3cd-69e191baba4e
# {
#   "status": "ERROR",
#   "reason": "LNURL Transaction id or amount not supplied"
# }
#
# https://livingroomofsatoshi.com/api/v1/lnurl/payreq/5ae9f8da-7b0a-4f11-b3cd-69e191baba4e?amount=10000
# {
#   "pr": "lnbc100n1pnds27wpp5ezf8nxtqthgwsfq4q03uwy4x5r5haskj274qv3nts9jyrwe30uhshp5egpedxstkfgez6xulwt57mw20f04juxrp2wkj0cxl2crsf6lftxscqzzsxqyz5vqsp57pghxsj0e4t2vapduzqxaktuvuzdtfx6zuy3t5npjreywydk9sfq9qxpqysgq8vuejquv29zn0r4pjjpn7g7x4ht6ynv08lznj3yqwun3f875fpcqnmtqwc6mggpkceccccdfg670ff05htmsxf5chfrm9knjau627ygqvvn7ye",
#   "routes": []
# }
# @well_known_bp.route("/lnurlp/<string:account>", methods=["GET"])
# def lnurlp(account: str):
#     return {
#         "allowsNostr": true,
#         "callback": "https://livingroomofsatoshi.com/api/v1/lnurl/payreq/5ae9f8da-7b0a-4f11-b3cd-69e191baba4e",
#         "commentAllowed": 255,
#         "maxSendable": 100000000000,
#         "metadata": '[["text/plain","Pay to Wallet of Satoshi user: numericquiver54"],["text/identifier","numericquiver54@walletofsatoshi.com"]]',
#         "minSendable": 1000,
#         "nostrPubkey": "be1d89794bf92de5dd64c1e60f6a2c70c140abac9932418fee30c5c637fe9479",
#         "tag": "payRequest",
#     }


# Access-Control-Allow-Origin *
@well_known_bp.route("/nostr.json", methods=["GET"])
def nostr():
    data = {
        "names": {
            "ajrlewis": "ad1a216219eb17ef3f6cc28c288d86bd1d414ef1062475db716bb513ee8143a0"
        }
    }
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
