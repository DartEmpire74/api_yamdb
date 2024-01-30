from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
