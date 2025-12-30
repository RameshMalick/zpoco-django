from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/download/', views.download_product, name='download_product'),
    path('product/<int:product_id>/buy/', views.buy_product, name='buy_product'),
    path('add/', views.add_product, name='add_product'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
