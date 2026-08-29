class FinanceTrackerError(Exception):

    def __init__(self,message,error_code=None):
        super().__init__(message)

        self.message=message
        self.error_code=error_code


class ValidationError(FinanceTrackerError):

    def __init__(self,message):
        super().__init__(
            message=message,
            error_code="Validation_Error"
        )

class InvalidTransactionError(FinanceTrackerError):

    def __init__(self,message):
        super().__init__(
            message=message,
            error_code="Invalid_Transaction"
        )

class DataConflictError(FinanceTrackerError):

    def __init__(self,message):
        super().__init__(
            message=message,
            error_code="Data_Conflict"
        )

class NotFoundError(FinanceTrackerError):

    def __init__(self,message):
        super().__init__(
            message=message,
            error_code="Not_Found"
        )