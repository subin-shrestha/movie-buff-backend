from rest_framework.viewsets import ReadOnlyModelViewSet

from helpers.viewsets import ResponseMixin
from helpers.permissions import IsVerified
from quiz.models import UserAggregate
from quiz.serializers import UserAggregateSerializer


class UserAggregateAPI(ResponseMixin, ReadOnlyModelViewSet):
	lookup_field = "idx"
	queryset = UserAggregate.objects.all()
	serializer_class = UserAggregateSerializer
	permission_classes = [IsVerified]

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.select_related('user').order_by('-total_score')
		return queryset