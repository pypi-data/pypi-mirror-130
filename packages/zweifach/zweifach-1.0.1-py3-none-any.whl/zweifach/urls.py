from django.urls import path
from django.views.decorators.cache import never_cache

from zweifach import views


urlpatterns = [
    path('verify/', never_cache(views.verify), name='zweifach_verify'),
    path('setup/', never_cache(views.setup), name='zweifach_setup'),
]
