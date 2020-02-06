# -*- coding: utf-8 -*-
from .views import get_page
from django.urls import path

urlpatterns = [
    path('<path:url>', get_page, name="page"),
]