from .transaction_input import TransactionInput
from .transaction_output import TransactionOutput
from .utils import uint4, varint


class Transaction:
    def __init__(self, blockchain):
        self.seq = 0
        self.version = uint4(blockchain)
        self.input_count = varint(blockchain)
        self.inputs = []
        for i in range(self.input_count):
            input = TransactionInput(blockchain)
            self.inputs.append(input)

        self.output_count = varint(blockchain)
        self.outputs = []
        for i in range(self.output_count):
            output = TransactionOutput(blockchain)
            self.outputs.append(output)

        self.lockTime = uint4(blockchain)

    def to_dict(self):
        return {
            'Transaction Sequence Number': self.seq + 1,
            'Transaction Version': self.version,
            'Transaction Input Count': self.input_count,
            'Input transactions': [input.to_dict() for input in self.inputs],
            'Transaction Output Count': self.output_count,
            'Output transactions': [output.to_dict() for output in self.outputs],
            'Lock Time': self.lockTime
        }
