from django.urls import path

from petstagram.common.views import LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing page')
]
