from . import views
from django.conf.urls import url

app_name = 'work'

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^unload', views.unload, name='unload'),  # создать шаблон
]