from django.urls import path
from .views import *

    
urlpatterns = [
    path('',TaskView.as_view(),name="task"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/<int:user_pk>/<str:token>/', VerifyEmailView.as_view(), name='verify'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('create/', CreateTask.as_view(), name='create'),
    path('task/', TaskView.as_view(), name='task'),
    path('delete/<int:pk>/',TaskDeleteView.as_view(), name='delete'),
]