# from .models import CustomUser 


# class EmailAuthBackend(object):
#     """
#     Authenticate using an e-mail address.
#     """
#     def Authenticate(self, request, username=None, password=None):
#         try:
#             user = CustomUser.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except CustomUser.DoesNotExist:
#             return None
