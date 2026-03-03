
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
    
    # Community routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('community/create/', views.create_community, name='create_community'),
    path('community/<int:community_id>/join/', views.join_community, name='join_community'),
    path('community/<int:community_id>/leave/', views.leave_community, name='leave_community'),
    path('community/<int:community_id>/manage/', views.manage_community, name='manage_community'),
    path('community/<int:community_id>/delete/', views.delete_community, name='delete_community'),
    path('community/<int:community_id>/member/<int:user_id>/remove/', views.remove_member, name='remove_member'),

    # Admin routes
    path('manage/', views.manage_polls, name='manage_polls'),
    path('manage/create/', views.create_poll, name='create_poll'),
    path('manage/<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('manage/<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
    path('manage/<int:poll_id>/toggle/', views.toggle_poll_status, name='toggle_poll_status'),
    path('manage/<int:poll_id>/add-choice/', views.add_choice, name='add_choice'),
    path('manage/choice/<int:choice_id>/delete/', views.delete_choice, name='delete_choice'),
]