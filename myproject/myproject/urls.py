"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app import views 
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.index), name='home'),
    path('login/', csrf_exempt(views.index_login), name='login'),
    path('logout/', csrf_exempt(views.index_logout), name='logout'),
    path('admin/', admin.site.urls),
    path('user/login/saml/', csrf_exempt(views.login_saml), name="user_login_saml"),
    path('user/logout/', csrf_exempt(views.logout_saml), name="user_logout_saml")
]