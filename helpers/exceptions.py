
class CustomException(Exception):
	""" Base exception for every custom exception. """
	def __init__(self, message, error_key='custom_error'):
		super().__init__(message, error_key)
		self.message = message
		self.error_key = error_key


class UserAlreadyVerified(CustomException):
	def __init__(self, message="User has already Verified.", error_key='already_verified'):
		super().__init__(message, error_key)


class AlreadyExists(CustomException):
	def __init__(self, message="Object is already exists.", error_key='already_exists'):
		super().__init__(message, error_key)
