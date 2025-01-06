from django.urls import path 
from . import views 

urlpatterns=[
   
    path('menu-items/', views.Menu_items.as_view(
		{
            'get': 'list',
            'post': 'create',

        })),

    path('categories/', views.Categories.as_view(
        {
            'get':'list',
            'post':'create',
        }
    )),
    path('menu-items/<int:pk>/',views.Menu_items.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })),
    path('groups/manager/users/', views.Manager.as_view(
        {
            'get':'list',
            'post':'create',
        })),
    path('groups/manager/users/<int:id>/',views.Manager.as_view(
        {
            'delete': 'destroy',
        })),
    #For the delivery crew
    path('groups/delivery-crew/users/', views.deliveryCrew.as_view(
        {
            'get':'list',
            'post':'create',
        })),
    path('groups/delivery-crew/users/<int:id>/',views.deliveryCrew.as_view(
        {
            'delete': 'destroy',
        })),

    path('cart/menu-items/', views.CartViewSet.as_view(
        {
            'get':'list',
            'post':'create',
            'delete':'destroy',
        })), 

    path('orders/', views.Orders.as_view(
        {
            'get':'list',
            'post':'create',
            
        })),
    path('orders/<int:id>/', views.Orders.as_view(
        {
            'get':'retrieve',
            'put':'update',
            'patch':'partial_update',
            'delete':'destroy',
        })),
    ]

