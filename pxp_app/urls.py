from django.urls import path

from pxp_app import views

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    path('add-ticket/', views.add_ticket_view, name='add-ticket-view'),
    path('manage-tickets/', views.manage_tickets_view, name='manage-tickets-view'),
    path('ticket/<int:pk>/', views.ticket_detail_view, name='ticket-detail-view'),
    path('delete-ticket/<int:pk>/', views.ticket_delete_view, name='ticket-delete-view'),
]