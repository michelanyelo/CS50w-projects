from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # entry page
    path("wiki/<str:title>", views.get_content, name="entry"),
    # search
    path("search/", views.search, name="search"),
    # new entry
    path("new/", views.new_entry, name="new_entry"),
    # edit and save entry
    path("edit/<str:title>", views.edit_entry, name="edit_entry"),
    # random entry
    path("rand", views.random_entry, name="random_entry")

]
