from django.urls import path

from .views import ProfileDetailView, ProfileUpdate

urlpatterns = [
    path('profile=<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update=<int:pk>/', ProfileUpdate.as_view(), name='profile_update')
]
