import struct
import json
from .utils import varint
from .transaction import Transaction
from .block_header import BlockHeader


class Block:
    def __init__(self, blockchain):
        try:
            self.block_header = BlockHeader(blockchain)
            self.tx_count = varint(blockchain)
            self.txs = []
            for i in range(self.tx_count):
                tx = Transaction(blockchain)
                tx.seq = i
                self.txs.append(tx)
        except struct.error as ex:
            # The binary data get from webbtc may be incomplete
            pass

    def __repr__(self):
        return json.dumps({
            'Count of transactions': self.tx_count,
            'Block Header': self.block_header.__dict__,
            'Transactions': [tx.to_dict() for tx in self.txs[:5]]
        }, indent=4)
