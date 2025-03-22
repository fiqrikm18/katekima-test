from django.urls import path
from rest_framework.routers import format_suffix_patterns

from ..views.sell_view import SellView

SELL_VIEW_INDEX_ROUTE = {
    'get': 'list',
    'post': 'create'
}

SELL_VIEW_DETAIL_ROUTE = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
}

SELL_VIEW_DETAIL_purcahse_ROUTE = {
    'get': 'get_detail_sell',
    'post': 'crate_detail_sell'
}

urlpatterns = format_suffix_patterns([
    path('', SellView.as_view(SELL_VIEW_INDEX_ROUTE)),
    path('<str:code>', SellView.as_view(SELL_VIEW_DETAIL_ROUTE)),
    path('<str:code>/details', SellView.as_view(SELL_VIEW_DETAIL_purcahse_ROUTE)),
])
