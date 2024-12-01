"""
Custom API response codes for better error handling and maintenance of the codebase.
"""


class APIResponseCode(object):
    # Existing codes
    FAILURE = {"code": -1, "message": 'General failure'}  # General logic error
    SUCCESS = {"code": 0, "message": 'Success'}  # Successful response
    SERVER_ERROR = {"code": 1, "message": 'Server error'}  # Unexpected error during handling the request

    # Add new error codes
    INVALID_TOKEN = {"code": 2, "message": 'Invalid token or token verification failed'}
    TOKEN_EXPIRED = {"code": 3, "message": 'Token has expired'}
    MISSING_TOKEN = {"code": 4, "message": 'Missing access token'}
    NOT_FOUND = {"code": 5, "message": 'Resource not found'}
    INVALID_COORDINATES = {"code": 6, "message": 'Invalid latitude or longitude values'}
    API_ERROR = {"code": 7, "message": 'External API error'}
    RATE_LIMIT_EXCEEDED = {"code": 8, "message": 'Rate limit exceeded'}
    INVALID_CREDENTIALS = {"code": 9, "message": 'Invalid username or password'}
    VALIDATION_ERROR = {"code": 10, "message": 'Data validation error'}
    DATABASE_ERROR = {"code": 11, "message": 'Database operation error'}

    @classmethod
    def is_success(cls, code):
        return code == cls.SUCCESS

    @classmethod
    def is_failure(cls, code):
        return code != cls.SUCCESS
