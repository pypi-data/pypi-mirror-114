from django.conf.urls import url
from request_proxy.views import proxy

urlpatterns = [url('^', proxy, name="proxy")]