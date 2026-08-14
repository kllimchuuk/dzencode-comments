from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from comments.views import CaptchaView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/captcha/", CaptchaView.as_view(), name="captcha"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
