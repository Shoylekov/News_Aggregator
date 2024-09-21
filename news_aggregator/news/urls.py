from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('preferences/', views.preferences, name='preferences'),
    path('save_article/', views.save_article, name='save_article'),
    path('saved_articles/', views.saved_articles, name='saved_articles'),
    path('remove_saved_article/<int:article_id>/', views.remove_saved_article, name='remove_saved_article'),

]

