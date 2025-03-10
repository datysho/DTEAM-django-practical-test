from django.contrib import admin
from django.urls import path, include
from main import views as main_views
from rest_framework import routers
from main.views_api import CVViewSet


router = routers.DefaultRouter()
router.register(r'cv', CVViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.cv_list, name='cv_list'),
    path('cv/<int:id>/', main_views.cv_detail, name='cv_detail'),
    path('cv/<int:id>/pdf/', main_views.cv_pdf, name='cv_pdf'),
    path('api/', include(router.urls)),
]
