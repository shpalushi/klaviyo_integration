from django.urls import include, path
from rest_framework import routers
from .views import KlaviyoData

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('send-data-klaviyo/', KlaviyoData.as_view())
]
