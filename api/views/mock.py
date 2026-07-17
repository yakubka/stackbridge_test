from rest_framework.views import APIView
from rest_framework.response import Response

from ..authentication import JWTAuth
from ..permissions import make_perm

PRODUCTS = [
    {'id': 1, 'name': 'Widget A', 'price': 9.99},
    {'id': 2, 'name': 'Widget B', 'price': 19.99},
    {'id': 3, 'name': 'Widget C', 'price': 4.99},
]

STORES = [
    {'id': 1, 'name': 'Downtown', 'address': '123 Main St'},
    {'id': 2, 'name': 'Uptown', 'address': '456 Oak Ave'},
]

ORDERS = [
    {'id': 1, 'product_id': 1, 'quantity': 2, 'status': 'pending'},
    {'id': 2, 'product_id': 2, 'quantity': 1, 'status': 'shipped'},
]


class ProductsView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [make_perm('products', 'can_read')]

    def get(self, request):
        return Response(PRODUCTS)


class StoresView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [make_perm('stores', 'can_read')]

    def get(self, request):
        return Response(STORES)


class OrdersView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [make_perm('orders', 'can_read')]

    def get(self, request):
        return Response(ORDERS)
