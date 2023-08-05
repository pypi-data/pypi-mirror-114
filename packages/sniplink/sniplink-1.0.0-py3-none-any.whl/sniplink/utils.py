class SnipLinkError(Exception):
    """
    Represents a shiplink error.
    """
    def __init__(self, reason):
        self.reason = str(reason)

    def __str__(self):
        return repr(self.reason)


class Utils:
    def __init__(self):
        pass
