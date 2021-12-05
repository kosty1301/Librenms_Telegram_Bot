class LibrenmsApiError(Exception):
    """Could connect to LIBRENMS API"""
    def __str__(self):
        return 'Could connect to LIBRENMS API'
