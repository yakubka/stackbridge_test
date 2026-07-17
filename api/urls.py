from django.urls import path

from .views.auth import RegisterView, LoginView, LogoutView
from .views.users import ProfileView
from .views.admin import RulesView, RuleDetailView
from .views.mock import ProductsView, StoresView, OrdersView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('me/', ProfileView.as_view()),
    path('admin/rules/', RulesView.as_view()),
    path('admin/rules/<int:pk>/', RuleDetailView.as_view()),
    path('products/', ProductsView.as_view()),
    path('stores/', StoresView.as_view()),
    path('orders/', OrdersView.as_view()),
]
