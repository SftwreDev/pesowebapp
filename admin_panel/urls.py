from django.urls import path

from .views import *

urlpatterns = [
    path("admin-page/", admin_page, name="admin_page"),
    path("account-accept/<int:pk>", accept_account, name="accept_account"),
    path("account-unaccept/<int:pk>", unaccept_account, name="unaccept_account"),
    path("account-view/<int:pk>", account_view, name="account_view")
]