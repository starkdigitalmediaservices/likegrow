from django.urls import re_path,path
from django.conf.urls import include 
from django.conf import settings

from like_grow_app.views.change_password import ChangePasswordView
from .views.login import LoginViewSet
from .views.forget_password import ForgotPasswordView
from .views.verify_otp import VerifyPasswordView
from .views.reset_password import ResetPasswordView
from .views.logout import LogoutView
from .views.user_impersonate import ImpersonateView
from .views.login_verify_otp import LoginVerifyView

""" User login/ add/ logout profile urls"""
urlpatterns = [
    re_path(r'^login/$', LoginViewSet.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
]

""" User forget_password/ verify_otp/ reset_password/ profile urls"""
urlpatterns += [
    re_path(r'^forget-password/$', ForgotPasswordView.as_view()),
    re_path(r'^verify-otp/$', VerifyPasswordView.as_view()),
    re_path(r"^change-password/$", ChangePasswordView.as_view({"post": "change_password"})),
    re_path(r'^reset-password/$', ResetPasswordView.as_view()),
]

""" User impersonate"""
urlpatterns += [
    re_path(r'^user-impersonate/(?P<id>.+)/$', ImpersonateView.as_view({'get': 'retrieve'})),
]

""" login-verify-otp"""
urlpatterns += [
    re_path(r'^login-verify-otp/$', LoginVerifyView.as_view({'get': 'retrieve'})),
]

        

from .views.student import StudentView

''' Student '''
urlpatterns += [
    re_path(r'^student/$', StudentView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
    re_path(r'^student/(?P<id>.+)/$', StudentView.as_view({'get': 'retrieve', 'delete': 'delete', 'put': 'partial_update'})),
]

# from django.urls import path
# from like_grow_app.views.facebook_signup import facebook_signup

# urlpatterns = [
#     path('facebook/signup/', facebook_signup, name='facebook_signup'),
#     # Add other URLs
# ]

from rest_framework.routers import DefaultRouter
from like_grow_app.views.facebook_signup import FacebookUserViewSet

# router = DefaultRouter()
# router.register(r'facebook-users', FacebookUserViewSet)

# urlpatterns = router.urls
from .views.student import StudentView

''' Student '''
urlpatterns += [
    re_path(r'^sign-up/$', FacebookUserViewSet.as_view({'post': 'create' })),
    # re_path(r'^student/(?P<id>.+)/$', StudentView.as_view({'get': 'retrieve', 'delete': 'delete', 'put': 'partial_update'})),
]
