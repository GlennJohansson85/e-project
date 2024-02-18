from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Import our settings from <- this
from django.conf.urls.static import static # Import our static function from <- this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # And then use the static function to add the MEDIA_URL to our list of URLs.
