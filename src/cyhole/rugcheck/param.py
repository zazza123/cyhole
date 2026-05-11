from ..core.param import CyholeParam


class RugcheckAnalyticsWindow(CyholeParam):
    """
    Time window options for the analytics endpoint.

    Attributes:
        H24: 24-hour window.
        D1: 1-day window.
        D7: 7-day window (default).
        D30: 30-day window.
    """
    H24 = "24h"
    D1 = "1d"
    D7 = "7d"
    D30 = "30d"
