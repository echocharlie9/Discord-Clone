from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# defining url paths
adminPath = 'admin/'
authPath = 'auth/'
lobby = 'lobby/'
room = 'room/'

# urlpatterns (url paths mapped to views or other urlpatterns)
urlpatterns = [
    path('/', TemplateView.as_view(template_name='index.html')),
    path(adminPath, admin.site.urls),
    path(authPath, include('apps.myauth.api.urls')),
    path(lobby, include('apps.lobby.api.urls')),
    path(room, include('apps.room.api.urls'))
]