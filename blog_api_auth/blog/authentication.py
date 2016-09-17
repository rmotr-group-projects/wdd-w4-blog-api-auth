from rest_framework import exceptions, authentication, permissions

from django.core.exceptions import ValidationError

from blog.models import User, validate_authkey


class UserAccesskeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey using GET parameters"""

    def authenticate(self, request):
        # If an access key was not passed, don't authenticate
        if 'accesskey' in request.GET:
            access_key = request.GET['accesskey']
        else:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.'    
            )
        
        try:
            validate_authkey(access_key)
        except ValidationError:
            raise exceptions.AuthenticationFailed('Invalid Accesskey')
        
        try:
            user = User.objects.get(accesskey=access_key)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        
        # Authenticate if the request method is safe.
        if request.method in permissions.SAFE_METHODS:
            return (user, None)
        else:
            return None
        


class UserSecretkeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey and secretkey
       Accesskey should be sent in query_params, and Secretkey in
       custom X-Secret-Key header.
    """

    def authenticate(self, request):
        # We already passed the access key authentication step
        access_key = request.GET['accesskey']
        
        # If a secret key was not passed, don't authenticate
        secret_key = request.META.get('HTTP_X_SECRET_KEY')
        if not secret_key:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.'    
            )
        
        try:
            validate_authkey(secret_key)
        except ValidationError:
            raise exceptions.AuthenticationFailed('Invalid Secretkey')
        
        try:
            user = User.objects.get(
                accesskey=access_key,
                secretkey=secret_key
            )
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        
        return (user, None)