from django.urls import path
from .views import *

urlpatterns = [
    path('', AdvertListView.as_view(), name='advert_list'),
    path('list-user/', AdvertListViewUser.as_view(), name='advert_list_user'),
    path('search/', AdvertSearch.as_view(), name='advert_list_search'),
    path('detail/<slug:slug>/', AdvertDetailView.as_view(), name='advert_detail'),
    path('create/', AdvertCreate.as_view(), name='advert_create'),
    path('update/<slug:slug>/', AdvertUpdate.as_view(), name='advert_update'),
    path('delete/<slug:slug>/', AdvertDelete.as_view(), name='advert_delete')

]
