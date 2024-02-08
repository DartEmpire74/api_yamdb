from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from api.permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class PatchOnlyMixin:
    http_method_names = ('get', 'post', 'patch', 'delete', )
