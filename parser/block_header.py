from .utils import uint4, hash32, time, calc_difficulty


class BlockHeader:
    def __init__(self, blockchain):
        self.version = hex(uint4(blockchain))
        self.previous_block_hash = hash32(blockchain)
        self.merkle_root = hash32(blockchain)
        self.time = time(blockchain)
        self.bits = uint4(blockchain)
        self.difficulty = calc_difficulty(self.bits)
        self.nonce = uint4(blockchain)