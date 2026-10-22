class ApplicationError(Exception):
    "Basic Application layer Exception."



class ResourceNotFoundError(ApplicationError):
    "Requested resourse not found."



class BusinessRuleError(ApplicationError):
    "Business-rule violation."



class ConflictError(ApplicationError):
    "The operation conflicts with current data state."