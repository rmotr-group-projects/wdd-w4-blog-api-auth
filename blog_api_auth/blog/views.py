from django.contrib.auth.hashers import make_password

from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response

from blog.models import User, Entry, Blog
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import UserSerializer, EntrySerializer, BlogSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username',)
    ordering_fields = ('id',)

    def update(self, request, *args, **kwargs):
        # you will probably do some custom actions about the `password` here
        payload = request.POST
        if 'password' in payload:
            payload['password'] = make_password(payload['password'])
        request.user.update(**payload)
        content = {'status': 'request was permitted'}
        return Response(content)

    def create(self, request, *args, **kwargs):
        # you will probably do some custom actions about the `password` here
        payload = request.POST
        if 'password' in payload:
            payload['password'] = make_password(payload['password'])
        request.user.create(**payload)
        content = {'status': 'request was permitted'}
        return Response(content)


class BlogViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('id',)


class EntryViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('headline',)
    ordering_fields = ('id',)
    # configure the custom permission class here
    permission_classes = (IsOwnerOrReadOnly,)
