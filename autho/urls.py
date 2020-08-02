from django.urls import re_path as url

from autho import views


urlpatterns = [
    url('api/signup', views.Signup, name="signup")
]