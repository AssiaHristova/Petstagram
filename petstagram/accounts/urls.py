from django.urls import path

from petstagram.accounts.views import logout_user, RegisterView, ProfileDetailsView, LogInView

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailsView.as_view(), name='profile details')
]
