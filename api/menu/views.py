from django.shortcuts import render
from rest_framework import viewsets, filters , permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import MenuItem
from .serializers import MenuItemSerializer

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True  # يسمح للجميع بالقراءة
        return request.user and request.user.is_staff  # فقط الـ admin يعدل

class MenuItemViewSet(viewsets.ModelViewSet):
    """
    CRUD كامل لعناصر القائمة.
    يتيح فلترة الاسم أو السعر، مع بحث نصّي جزئي على الاسم.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'name']        #فلترة دقيقة بالقيمة
    search_fields    = ['name']           # بحث نصي جزئي
    ordering_fields  = ['price', 'name']  #  لتحديد الحقول التي يمكن للمستخدم ترتيب النتائج بناءً عليها.

