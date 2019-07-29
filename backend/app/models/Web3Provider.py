from web3 import Web3, HTTPProvider, eth

from .. import app
from ..misc import abi, wait_in_other_thread
w3 = Web3(HTTPProvider(app.config.get("WEB3_HTTP_PROVIDER_ADDRESS")))

Merkatuan = w3.eth.contract(Web3.toChecksumAddress(app.config.get("MEMESMERKATUAN_ADDRESS")), abi=abi.MERKATUAN_ABI)


def send_payable_transaction(tx, public, private):
    tx['nonce'] = w3.eth.getTransactionCount(public)
    signed_txn = w3.eth.account.signTransaction(tx, private)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return signed_txn.hash

def onReciept(hsh, callback):
    def wrapper():
        return w3.eth.waitForTransactionReceipt(hsh)
    wait_in_other_thread(wrapper, callback)
