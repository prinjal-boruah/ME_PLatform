from django.urls import path, re_path
from app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # re_path(r'^.*\.html', views.pages, name='pages'),
    path('', views.index, name='home'),
    path('login/', views.loginView, name = "login"),
    path('register/', views.register_user, name = "register"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path('addorg/', views.addOrgView, name = "addorg"),
    path('addcard/', views.addCardView, name = "addcard"),
    path('addproject/', views.addProjectView, name = "addproject"),
    path('selectplan/', views.selectPlanView, name = "selectplan"),
    path('confirmation/', views.confirmationView, name = "confirmation"),

    path('postdetails/<int:pk>/', views.postMEdetails, name = "postdetails"),
]
