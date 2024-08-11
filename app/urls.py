from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),  # Added logout path
    path('home/', views.home, name='home'),
    # path('communities/', views.community_list, name='community_list'),
    path('communities/<int:community_id>/',
         views.community_detail, name='community_detail'),
    path('communities/<int:community_id>/post/',
         views.create_post, name='create_post'),
    path('communities/<int:community_id>/chat/',
         views.create_chat_message, name='create_chat_message'),
    path('communities/<int:community_id>/join/', views.join_community,
         name='join_community'),
    path('communities/<int:community_id>/leave/', views.leave_community,
         name='leave_community'),

    path('seek-help/', views.seek_help, name='seek_help'),
    path('seekers/', views.seekers, name='seekers'),
    path('give-help/<int:pk>/', views.give_help, name='give_help'),
    path('histdata', views.dataH, name='histdata'),
    path('educate', views.Elearn, name='educate'),
    path('map', views.HeatMap, name='map'),
    # path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/ask/', views.ask_chatbot, name='ask_chatbot'),
    path('contacts', views.Contacts, name='contacts'),
    path('weather', views.Weather, name='weather'),
]
