
ERR_ONVIF_UNKNOWN = 1

class ONVIFError(Exception):
    """ONVIF Exception class."""

    def __init__(self, err):
        self.reason = "Unknown error: " + str(err)
        self.code = ERR_ONVIF_UNKNOWN
        super().__init__(err)

    def __str__(self):
        return self.reason

class ONVIFUtilitiesError(ONVIFError):
    pass