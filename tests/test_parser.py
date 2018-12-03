import unittest
from parser.block import Block


class TestParser(unittest.TestCase):
    def test_valid_block(self):
        with open('./resources/000000000000000002775ff227222f47a46cad46b0f634db53c1a8737d7ecd41.bin', "rb") as file:
            b = Block(file)
        self.assertEqual(b.tx_count, 9)
        # Test block header
        block_header = b.block_header
        self.assertEqual(block_header.version, '0x20000000')
        self.assertEqual(block_header.previous_block_hash, "000000000000000002424db0163641940c9fd999ec897b412ce64e36d6ab7650")
        self.assertEqual(block_header.merkle_root, "29d000eee85f08b6482026be2d92d081d6f9418346e6b2e9fe2e9b985f24ed1e")
        self.assertEqual(block_header.time, "2016-12-17 19:07:59")
        self.assertEqual(block_header.bits, 402885509)
        self.assertEqual(block_header.nonce, 3814348197)
        self.assertEqual(block_header.difficulty, 310153855703.43335)
        # Test transaction
        first_transaction = b.txs[0]
        self.assertEqual(first_transaction.version, 1)
        self.assertEqual(first_transaction.lockTime, 0)
        self.assertEqual(first_transaction.input_count, 1)
        self.assertEqual(first_transaction.output_count, 1)
        # Test coin base
        first_input = first_transaction.inputs[0]
        self.assertEqual(first_input.prev_transaction_hash, "No Inputs (Newly Generated Coins)")
        self.assertEqual(first_input.prev_transaction_out_index, "none")
        first_output = first_transaction.outputs[0]
        self.assertEqual(first_output.address, "1ERSHV5douNTHuCnJj7uSJDtPvEKX2NZvZ")
        self.assertEqual(first_output.script_pubkey, "OP_DUP OP_HASH160 9338b976abdb1a5c8711ac57bb2417a98fdb8bac OP_EQUALVERIFY OP_CHECKSIG")
        self.assertEqual(first_output.value, 12.51665471)
        # Test normal transaction
        second_transaction = b.txs[1]
        second_input = second_transaction.inputs[0]
        self.assertEqual(second_input.prev_transaction_hash, "3539b599a5104cd5be4294907cd1a3e106e9c73f46d9d1bfe80ccceb71986283")
        self.assertEqual(second_input.prev_transaction_out_index, 0)
        self.assertEqual(second_input.signature_script, "3045022100ea916940af7b9b956a5bbca726a54648dd2cbc61de020f557a44cb42c3b8d3fd022051c95dc222576b841e"
                                                        "4a689b1400527beba5b9128b68eb2c6f567808df4ef45601210382fd762515b68a938074a17d8a2aa054a"
                                                        "60fb9594e2c92656a29244860dbf7c5")
        self.assertEqual(second_input.sequence_number, 4294967293)
        self.assertEqual(second_input.address, "1MnxApADqgUAnP384TKYrudVMmj6zRspSd")

    def test_invalid_block(self):
        with open('./resources/invalid.bin', "rb") as file:
            b = Block(file)
        self.assertFalse(hasattr(b, "block_header"))
        self.assertFalse(hasattr(b, "tx_count"))
        self.assertFalse(hasattr(b, "txs"))

    def test_p2sh_address(self):
        with open('./resources/000000000000000000f061205567dc79c4e718209a568879d66132e016968ac6.bin', "rb") as file:
            b = Block(file)
        transaction_output = b.txs[2].outputs[1]
        self.assertEqual(transaction_output.address, "3D9FUuyE4dUgYP4wywsEATcQ7nK3hyfHmb")
        self.assertEqual(transaction_output.script_pubkey, "OP_HASH160 7d9f8430aacddce58eb72a28557813136e92c2ea OP_EQUAL")


if __name__ == '__main__':
    unittest.main()
