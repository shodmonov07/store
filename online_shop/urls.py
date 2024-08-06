from django.urls import path

from online_shop import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='category_list_id'),
    path('detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_comment', views.add_comment, name='add_comment'),
    path('product/<int:product_id>/add_order', views.add_order, name='add_order'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product')
]


