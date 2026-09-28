from django.urls import path
from .views import PlaceOrderView, MyOrdersView

urlpatterns = [
    path('place/', PlaceOrderView.as_view()),
    path('my-orders/', MyOrdersView.as_view()),
]