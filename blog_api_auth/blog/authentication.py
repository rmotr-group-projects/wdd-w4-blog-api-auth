from rest_framework import exceptions, authentication, permissions

from django.core.exceptions import ValidationError

from blog.models import User, validate_authkey


class UserAccesskeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey using GET parameters"""

    def authenticate(self, request):
        if 'accesskey' not in request.query_params:
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
        # Check to see if accesskey is valid
        else:
            try:
                validate_authkey(request.query_params['accesskey'])
            except ValidationError:
                raise exceptions.AuthenticationFailed('Invalid Accesskey')
        
        try:
            user = User.objects.get(accesskey=request.query_params['accesskey'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user with that accesskey')
        return (user, None)


class UserSecretkeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey and secretkey
       Accesskey should be sent in query_params, and Secretkey in
       custom X-Secret-Key header.
    """

    def authenticate(self, request):
        if 'HTTP_X_SECRET_KEY' not in request.META:
            if request.method != "GET":
                raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
            return None
        # Check to see if accesskey is valid
        else:
            try:
                validate_authkey(request.META['HTTP_X_SECRET_KEY'])
            except ValidationError:
                raise exceptions.AuthenticationFailed('Invalid Secretkey')
        
        try:
            user = User.objects.get(secretkey=request.META['HTTP_X_SECRET_KEY'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user with that secretkey')
        return None
