from django.urls import re_path as url
from rest_framework.routers import SimpleRouter

from quiz import views

router = SimpleRouter()

router.register(r'api/user-aggregate', views.UserAggregateAPI, basename="user-aggregate")

urlpatterns = router.urls

