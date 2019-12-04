from django.urls import path
from . import views

app_name = "photo"
urlpatterns = [
    path('add', views.PhotoUploadView.as_view(), name="upload_photo"),
    path('list', views.PhotoListView.as_view(), name="list_photos"),
    path('detail/<int:pk>', views.PhotoDetail.as_view(), name="photo_detail"),
    path('delete/<int:pk>', views.DeletePhoto.as_view(), name="delete_photo"),
    path('remove-bg/<int:pk>', views.PhotoRemoveBG.as_view(), name="remove_bg")
]
