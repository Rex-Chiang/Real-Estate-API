from RealEstateApp.models import UserToken
from rest_framework import exceptions

# Use user name and current time to generate token key
def md5(user):
    import hashlib
    import time
    try:
        cur_time = str(time.time())
        print(1)
        m = hashlib.md5(bytes(user, encoding = "utf-8"))
        m.update(bytes(cur_time, encoding = "utf-8"))
        return m.hexdigest()
    except Exception as msg:
        raise Exception("Fail To Generate Token !")

# Use token key as authenticated way
class Authentication(object):
    def authenticate(self, request):
        token = request.query_params.get("token")
        token_obj = UserToken.objects.filter(token = token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("User Verification Failed !")
        return (token_obj.user, token_obj)

    # This function must exist
    def authenticate_header(self, request):
        pass

# Only the user that user level greater than 1 can pass
class AdvancedSearch(object):
    def has_permission(self, request, view):
        # Use request.user.username as prior condition to avoid anonymous user
        if request.user.username and request.user.user_level > 1:
            return True
        return False