from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    signup,
    token,
)


router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, 'category')
router_v1.register('genres', GenreViewSet, 'genre')
router_v1.register('titles', TitleViewSet, 'title')
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
router_v1.register('users', UserViewSet, basename='users')

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token')
]

api_v1_urls = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_patterns))
]

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
