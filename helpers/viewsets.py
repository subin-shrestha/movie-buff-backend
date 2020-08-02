from rest_framework import status
from rest_framework.response import Response

class ResponseMixin:
	def api_success_response(self, data, status=status.HTTP_200_OK):
		return Response(data, status)

	def api_error_response(self, data, status=status.HTTP_400_BAD_REQUEST):
		return Response(data, status)
