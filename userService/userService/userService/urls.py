"""
URL configuration for userService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.views import TokenView

from userService.view import home_view
import oauth2_provider.views as oauth2_views

urlpatterns = [
    # path('', home_view, name='home'),
    # path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    path("admin/", admin.site.urls),

    path("", include("userservices.urls")),
    path("o/", include("oauth2_provider.urls")),
    # path('o/token/', csrf_exempt(TokenView.as_view()))
    # path('o/token/', csrf_exempt(oauth2_views.TokenView.as_view()))

]
