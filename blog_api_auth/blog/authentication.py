from rest_framework import exceptions, authentication, permissions

from django.core.exceptions import ValidationError

from blog.models import User, validate_authkey


class UserAccesskeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey using GET parameters"""

    def authenticate(self, request):
        # implement your logic here
        # import pdb; pdb.set_trace()
        if not request.GET.get('accesskey'):
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
        authkey = request.GET['accesskey']
        try:
            validate_authkey(authkey)
            user = User.objects.get(accesskey=authkey)
            return user, 'accesskey'
        except:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')
            # pass


class UserSecretkeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey and secretkey
       Accesskey should be sent in query_params, and Secretkey in
       custom X-Secret-Key header.
    """

    def authenticate(self, request):
        # implement your logic here
        # print(request.method)
        if not request.META.get('HTTP_X_SECRET_KEY'):
            # print(request.META)
            # print(request.method)
            if request.method == 'POST' or request.method == 'DELETE' or \
                            request.method == 'PUT' or request.method == 'PATCH':
                # print('hello')
                raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
            return None
        user, auth = UserAccesskeyAuthentication().authenticate(request)
        if user.secretkey == request.META.get('HTTP_X_SECRET_KEY'):
            return user, 'secretkey'
        raise exceptions.AuthenticationFailed('Invalid Secretkey')
