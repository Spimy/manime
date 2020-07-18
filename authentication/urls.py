from django.conf.urls import url
from .views import RegisterView

app_name = 'authentication'
urlpatterns = [
    url('register/', RegisterView.as_view(), name='register')
]
