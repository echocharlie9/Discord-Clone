from rest_framework import routers

# import views that will be mapped to url paths
from .views import LobbyViewSet

router = routers.SimpleRouter()
router.register(r'', LobbyViewSet)
urlpatterns = router.urls
