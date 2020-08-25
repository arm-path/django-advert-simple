from os import name
from django.urls import path
from .views import GalleryListView, GalleryDetailView, GalleryCreate, GalleryUpdate, GalleryDelete
from .views import ImageCreate, ImageDelete

urlpatterns = [
    path('', GalleryListView.as_view(), name='gallery_list'),
    path('detail/<slug:slug>/', GalleryDetailView.as_view(), name='gallery_detail'),
    path('create/gallery/', GalleryCreate.as_view(), name='gallery_create'),
    path('update/gallery/<slug:slug>/',
         GalleryUpdate.as_view(), name='gallery_update'),
    path('delete/gallery/<slug:slug>/',
         GalleryDelete.as_view(), name='galery_delete'),
    path('add-to-gallery/<slug:slug>/image/', ImageCreate.as_view(), name='image_create'),
    path('delete-from-gallery/<str:gallery>/<int:pk>/', ImageDelete.as_view(), name='image_delete' )
]
