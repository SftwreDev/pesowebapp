from django.urls import path
from .views import *

urlpatterns = [
    path("announcement-list", announcement_list, name="ann-list"),
    path("announcement-add", announcement_add, name="ann-add"),
    path("announcement-view/<int:pk>", announcement_view, name="ann-view"),
    path("announcement-update/<int:pk>", announcement_update, name="ann-update"),
    path("announcement-delete/<int:pk>", announcement_delete, name="ann-delete")
]