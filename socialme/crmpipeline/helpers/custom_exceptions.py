from rest_framework.exceptions import APIException

class EditException(APIException):
    """
    This exception is raised when a user attempts to perform an action that requires admin level
    permission, but the user is not authorized.
    Attributes:
        status_code (int): The HTTP status code associated with the exception (403 - Forbidden).
        default_detail (str): The default error detail message.
        default_code (str): The default error code.
    """

    status_code = 403
    default_detail = "you do not have the necessary permissions to perform this action."
    default_code = "forbidden"
