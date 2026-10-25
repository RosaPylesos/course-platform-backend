class ApplicationError(Exception):
    "Basic Application layer Exception."

class ResourceNotFoundError(ApplicationError):
    "Requested resourse was not found."

class AccessDeniedError(ApplicationError):
    "User's access to resource is prohibited."

class BusinessRuleError(ApplicationError):
    "Business-rule violation."

class ConflictError(ApplicationError):
    "The operation conflicts with current data state."

class InvalidInputError(ApplicationError):
    "The provided input is ivalid."