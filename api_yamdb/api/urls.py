from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import (
    CommentViewSet, ReviewViewSet,
    CategoryViewSet, GenreViewSet, TitleViewSet)


router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='title-reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='review-comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
