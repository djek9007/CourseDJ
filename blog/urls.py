from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [

    # path('', views.PostListView.as_view()),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='tag'),
    path('<slug:category_slug>/', views.PostListView.as_view(), name='category'),
    path('<slug:category>/<slug:slug>/', views.PostDetailView.as_view(), name='detail_post'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
