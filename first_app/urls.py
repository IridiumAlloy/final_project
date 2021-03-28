from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('welcome', views.welcome),
    path('logout', views.logout),
    path('login', views.login),
    path('user_page/<int:user_id>', views.user_page),
    path('edit/<int:user_id>', views.edit),
    path('legal_aid', views.legal_aid),
    path('view/<int:statute_id>', views.il_jca),
    path('add_subsection', views.add_subsection),
    path('save/<int:subsection_id>', views.save_section),
    path('saved/<int:user_id>', views.saved_stat)
]