from django.urls import path

from userservices.views.authView import AuthView
from userservices.views.roleView import RoleViewSet
from userservices.views.userView import UserView
from userservices.views.validateTokenForProService import validate_token

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('users/<int:pk>', UserView.as_view(), name='user_detail'),
    path('users/<int:user_id>/roles', UserView.as_view(), name='user_roles'),
    path('roles', RoleViewSet.as_view(), name='roles'),

    path('auth/login', AuthView.as_view(), name='login'),
    path('auth/logout', AuthView.as_view(), name='logout'),
    path('auth/signup', AuthView.as_view(), name='signup'),
    # path('auth/validate', AuthView.as_view(), name='validate'),

    path('auth/validate_token', validate_token, name='validate'),


]

