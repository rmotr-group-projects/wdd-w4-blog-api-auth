from django.contrib.auth.hashers import make_password

from rest_framework import viewsets, mixins, filters, status, exceptions
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
        if request.auth != 'secretkey':
            raise exceptions.AuthenticationFailed()
        user = User.objects.filter(username=request.user.username)
        # print(request.POST)
        # print(request.POST.dict())
        # fields = {key: value for key, value in request.POST.items()}
        # print(fields)
        # print(user)
        user.update(**request.POST.dict())
        # user.first().save()
        if 'password' in request.POST:
            request.user.set_password(request.POST['password'])
            request.user.save(update_fields=['password'])
        return Response()
        # pass

    def create(self, request, *args, **kwargs):
        # you will probably do some custom actions about the `password` here
        if request.auth != 'secretkey':
            raise exceptions.AuthenticationFailed()
        # print(request.POST)
        User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                 accesskey=request.POST['accesskey'], secretkey=request.POST['secretkey'])
        return Response(status=status.HTTP_201_CREATED)


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
