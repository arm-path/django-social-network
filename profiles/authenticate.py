from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user_model = User.objects.get(username=username)
            if user_model.check_password(password):
                return user_model
            return None
        except(User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            user_model = User.objects.get(id=user_id)
            return user_model
        except user.DoesNotExists:
            return None


class EmailAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user_model = User.objects.get(email=username)
            if user_model.check_password(password):
                return user_model
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            user_model = User.objects.get(id=user_id)
            return user_model
        except User.DoesNotExist:
            return None
