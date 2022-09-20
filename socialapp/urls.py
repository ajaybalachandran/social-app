"""socialapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register("api/v1/posts", views.PostsView, basename="posts")
router.register("api/v2/posts", views.PostsModelView, basename='mposts')

router.register("accounts/signup", views.UsersView, basename="users")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('token', ObtainAuthToken.as_view())
    path('token', TokenObtainPairView.as_view()),  # generate jwt token using username and password
    path('token/refresh', TokenRefreshView.as_view()),  # generate jwt token using refresh-token
]+router.urls
