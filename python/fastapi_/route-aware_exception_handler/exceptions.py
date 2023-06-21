class AcmeApplicationException(Exception):
    """Base exception for Acme application"""
    error_code = "ACME_EXCEPTION"


class AnvilError(AcmeApplicationException):
    """Raised to indicate problems with the Anvil component"""
    error_code = "ANVIL_ERROR"


class TNTError(AcmeApplicationException):
    """Raised to indicate problems with the TNT component"""
    error_code = "TNT_ERROR"
