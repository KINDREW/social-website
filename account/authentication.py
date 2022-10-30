"""User authentication Backend Custom"""
from django.contrib.auth.models import User

class EmailAuthBackend(object):
    """Authenticate using Email Address"""
    def authenticate(self, request, username =  None, password = None):
        """Trying to authenticate"""
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        """Trying the Get"""
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
