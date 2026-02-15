class ServiceException(Exception):
    """Domain/service-level exception that controllers can convert to API responses."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
