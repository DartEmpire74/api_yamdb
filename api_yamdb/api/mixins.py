from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class PatchOnlyMixin:
    http_method_names = ('get', 'post', 'patch', 'delete', )
