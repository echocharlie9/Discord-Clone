from rest_framework import routers

# import views that will be mapped to url paths
from .views import RoomViewSet

router = routers.SimpleRouter()
router.register(r'', RoomViewSet)
urlpatterns = router.urls