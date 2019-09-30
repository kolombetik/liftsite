"""liftsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, patterns
from django.contrib import admin
from lifts import views
from lifts.models import LiftPart

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^parts$', views.parts, kwargs={'kind': LiftPart.LIFTPARTS}),
    url(r'^board$', views.parts, kwargs={'kind': LiftPart.LIFTBOARD}),
    url(r'^otis$', views.parts, kwargs={'kind': LiftPart.LIFTOTIS}),
    url(r'^contacts$', views.contacts),
    url(r'^part/(?P<part_id>[0-9]+)$', views.part_page),
    url(r'^search/', views.search),
    url(r'^add-to-cart/', views.add_to_cart),
    url(r'^cart/', views.cart),
    url(r'^order/', views.order),
    url(r'^delivery$', views.delivery),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))