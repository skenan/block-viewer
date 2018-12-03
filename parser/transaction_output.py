from .utils import uint8, varint, format_hash, hash_to_address
from .opcode import OPCODE_NAMES


class TransactionOutput:
    def __init__(self, blockchain):
        self.value = uint8(blockchain) / 10 ** 8
        self.script_length = varint(blockchain)
        self.script = blockchain.read(self.script_length)
        self.script_pubkey = ''
        self.address = ''
        self.decode_script(self.script)

    def to_dict(self):
        return {
            'value': self.value,
            'length': self.script_length,
            'scriptPubkey': self.script_pubkey,
            'address': self.address
        }

    def decode_script(self, data):
        raw_hex = format_hash(data)
        op_idx = int(raw_hex[0:2], 16)
        # For now, we only parse P2PKH, P2SH
        if op_idx in OPCODE_NAMES and OPCODE_NAMES[op_idx] in ['OP_DUP', 'OP_HASH160']:
            op_code = OPCODE_NAMES[op_idx]

            if op_code == 'OP_DUP':
                op_code_two = OPCODE_NAMES[int(raw_hex[2:4], 16)]
                key_len = int(raw_hex[4:6], 16) * 2
                pubkey_hash = raw_hex[6: 6 + key_len]
                op_code_three = OPCODE_NAMES[int(raw_hex[6 + key_len: 6 + key_len + 2], 16)]
                op_code_four = OPCODE_NAMES[int(raw_hex[6 + key_len + 2:6 + key_len + 4], 16)]
                self.script_pubkey = "%s %s %s %s %s" % (op_code, op_code_two, pubkey_hash, op_code_three, op_code_four)
                self.address = str(hash_to_address(pubkey_hash))
            elif op_code == 'OP_HASH160':
                key_len = int(raw_hex[2:4], 16) * 2
                pubkey_hash = raw_hex[4: 4 + key_len]
                op_code_two = OPCODE_NAMES[int(raw_hex[4 + key_len:4 + key_len * 2 + 2], 16)]
                self.script_pubkey = "%s %s %s" % (op_code, pubkey_hash, op_code_two)
                self.address = str(hash_to_address(pubkey_hash, True))
        else:
            self.script_pubkey = raw_hex
