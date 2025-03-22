from django.urls import path
from rest_framework.routers import format_suffix_patterns

from ..views.purchase_view import PurchaseView

PURCHASE_VIEW_INDEX_ROUTE = {
    'get': 'list',
    'post': 'create'
}

PURCHASE_VIEW_DETAIL_ROUTE = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
}

PURCHASE_VIEW_DETAIL_purcahse_ROUTE = {
    'get': 'get_detail_purchase',
    'post': 'crate_detail_purchase'
}

urlpatterns = format_suffix_patterns([
    path('', PurchaseView.as_view(PURCHASE_VIEW_INDEX_ROUTE)),
    path('<str:code>', PurchaseView.as_view(PURCHASE_VIEW_DETAIL_ROUTE)),
    path('<str:code>/details', PurchaseView.as_view(PURCHASE_VIEW_DETAIL_purcahse_ROUTE)),
])
