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
    path("cv/<int:id>/send_email/", main_views.send_pdf_email, name="send_pdf_email"),
    path("cv/<int:id>/translate/", main_views.translate_cv, name="translate_cv"),
    path('api/', include(router.urls)),
    path('logs/', main_views.recent_logs, name='recent_logs'),
    path('settings/', main_views.settings_page, name='settings_page'),
]
