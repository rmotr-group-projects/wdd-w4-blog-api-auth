from rest_framework import exceptions, authentication, permissions

from django.core.exceptions import ValidationError

from blog.models import User, validate_authkey


class UserAccesskeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey using GET parameters"""

    def authenticate(self, request):
        # Grab username from META data
        username = request.META.get('X_USERNAME')
        print(username)
        # Check to see if accesskey is missing
        if 'accesskey' not in request.GET:
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
        # Check to see if accesskey is valid
        else:
            try:
                validate_authkey(request.GET['accesskey'])
            except ValidationError:
                raise exceptions.AuthenticationFailed('Invalid Accesskey')
        
        try:
            user = User.objects.get(username=username,accesskey=request.GET['accesskey'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)


class UserSecretkeyAuthentication(authentication.BaseAuthentication):
    """Authentication against User accesskey and secretkey
       Accesskey should be sent in query_params, and Secretkey in
       custom X-Secret-Key header.
    """

    def authenticate(self, request):
        # implement your logic here
        pass
