from django.urls import re_path as url
from rest_framework.routers import SimpleRouter

from autho import views


router = SimpleRouter()

router.register(r'api/user', views.UserAPI, basename="user")

urlpatterns = router.urls

