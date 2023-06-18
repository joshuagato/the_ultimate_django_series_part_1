from django.urls import path
from . import views
from .views import ProductList, ProductDetail, CollectionList, CollectionDetail

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    path('collections/', CollectionList.as_view()),
    path('collections/<int:pk>/', CollectionDetail.as_view(), name='collection-detail')
]
