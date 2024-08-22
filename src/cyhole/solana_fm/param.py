from ..core.param import CyholeParam

class SolanaFMBlocksPaginationType(CyholeParam):
    """
        Pagination type for Solana FM blocks.
    """
    BLOCK_NUMBER = "blockNumber"
    BLOCK_TIME = "blockTime"