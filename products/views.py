from rest_framework import viewsets
from .models import Product
from .serializer import ProductSerializer
from users.permissions import IsMerchant
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['price', 'stock']
    ordering_fields = ['price', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsMerchant()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)