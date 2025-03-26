"""
URL configuration for core app.

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

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.apis import (
    TaskViewSet, TaskAssignmentViewSet,
    UserViewSet, TeamViewSet, TeamRolesViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams/members', TeamRolesViewSet, basename='team-members')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'tasks/assign', TaskAssignmentViewSet, basename='task-assign')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Token Views
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('api/', include(router.urls)),
]
