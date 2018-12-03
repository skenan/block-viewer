from .utils import hash32, uint4, varint, format_hash, key_to_address


class TransactionInput:
    def __init__(self, blockchain):
        self.prev_transaction_hash = hash32(blockchain)
        self.prev_transaction_out_index = uint4(blockchain)
        self.script_length = varint(blockchain)
        self.script = blockchain.read(self.script_length)
        self.sequence_number = uint4(blockchain)
        self.signature_script = ''
        self.address = 'none'
        self.decode_script(self.script)

    def to_dict(self):
        return {
            'prev_transaction_hash': self.prev_transaction_hash,
            'prev_transaction_out_index': self.prev_transaction_out_index,
            'script': self.signature_script,
            'sequence_number': self.sequence_number,
            'address': self.address
        }

    def decode_script(self, data):
        raw_hex = format_hash(data)
        # Coinbase
        if 0xffffffff == self.prev_transaction_out_index:
            self.prev_transaction_hash = "No Inputs (Newly Generated Coins)"
            self.prev_transaction_out_index = 'none'
            self.signature_script = raw_hex
        else:
            self.signature_script = raw_hex[2:]
            sig_len = int(raw_hex[0:2], 16) * 2
            key_len = int(raw_hex[2 + sig_len: 2 + sig_len + 2], 16) * 2
            pubkey = raw_hex[2 + sig_len + 2:2 + sig_len + 2 + key_len]
            self.address = key_to_address(pubkey)
