from django.urls import path

from photo.views import DetailView, DeleteView, UpdateView
from .views import post_list, UploadView

app_name = 'photo'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('upload/', UploadView.as_view(), name='photo_upload'),
    path('detail/<int:pk>', DetailView.as_view(), name='photo_detail'),
    path('delete/<int:pk>', DeleteView.as_view(), name='photo_delete'),
    path('update/<int:pk>', UpdateView.as_view(), name='photo_update'),
]