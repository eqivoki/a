from django.urls import path

import debug_toolbar
from . import views

app_name = 'user_page'
urlpatterns = [
    path('panda/', views.panda, name='to_panda'),
    path('', views.index, name='index'),
    path('invest/<str:player>', views.to_MainWindow, name='to_MainWindow'),
    path('statisics/<str:player_nam>/', views.to_top_players, name='to_top_players'),
    path('test/', views.to_top_players, name='to_top_players'),
    path('test3/', views.to_personal_page, name='to_personal_page'),
    path('adminPage/', views.to_admin_page, name='to_admin_page'),
    path('testic/<str:play>/', views.next_step, name='next_step'),
    path('testic1/<str:player_name>/', views.make_choice, name='make_choice'),
    path('adminPage/<int:year>/', views.next_day_admin, name='next_day_admin'),
    path('top/<str:player>/', views.to_top, name='to_top'),
]

