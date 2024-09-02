from ...core.param import CyholeParam

class SolscanExportType(CyholeParam):
    """
        Export type for Solscan API.
    """
    TOKEN_CHANGE = "tokenchange"
    SOL_TRANSFER = "soltransfer"
    ALL = "all"