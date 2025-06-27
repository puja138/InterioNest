from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('shop/', views.shop_view, name='shop'),
    path('contact/', views.contact_view, name='contact'),
    path('blog/', views.blog_view, name='blog'),
    path('order/', views.order_view, name='order'),
    path('search/', views.search_view, name='search'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    
    # Admin Dashboard and Admin Tools
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('customers/', views.customer_list, name='customer_list'),  # ✅ Fixed name
    path('export-orders/', views.export_orders, name='export_orders'),
    path('search-orders/', views.search_orders, name='search_orders'),
]
