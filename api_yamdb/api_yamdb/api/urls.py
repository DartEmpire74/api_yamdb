from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    signup,
    token,
)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token')
]

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls))
]
