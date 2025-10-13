
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:poll_id>/results/', views.results, name='results'),
    
    # Admin routes
    path('manage/', views.manage_polls, name='manage_polls'),
    path('manage/create/', views.create_poll, name='create_poll'),
    path('manage/<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('manage/<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
    path('manage/<int:poll_id>/toggle/', views.toggle_poll_status, name='toggle_poll_status'),
]