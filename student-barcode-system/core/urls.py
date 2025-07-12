from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),

    # Student data access
    path('student/<str:roll_number>/', views.student_detail, name='student_detail'),
    path('profile/<str:roll_number>/', views.student_profile, name='student_profile'),

    path('student/<str:roll_number>/', views.student_detail, name='student_detail'),
    path('profile/<str:roll_number>/', views.student_profile, name='student_profile'),

]
