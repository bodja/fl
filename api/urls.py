from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'upload', views.FileUploadViewSet)

app_name = 'api'
urlpatterns = router.urls
