from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer, SiteSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class SiteViewset(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [permissions.IsAdminUser]
