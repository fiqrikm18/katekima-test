from django.urls import path
from rest_framework.routers import format_suffix_patterns

from .views.item_view import ItemView

ITEM_VIEW_INDEX_ROUTE = {
    'get': 'list',
    'post': 'create'
}

ITEM_VIEW_DETAIL_ROUTE = {
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update'
}

urlpatterns = format_suffix_patterns([
    path('', ItemView.as_view(ITEM_VIEW_INDEX_ROUTE)),
    path('<str:code>', ItemView.as_view(ITEM_VIEW_DETAIL_ROUTE)),
])
