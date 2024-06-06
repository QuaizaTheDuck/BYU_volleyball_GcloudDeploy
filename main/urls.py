from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('contact/', views.contact_page, name='contact'),
    path('faq/', views.faq_page, name='faq'),
    path('blog/', views.blog_page, name='blog'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)