from django.contrib import admin
from django.urls import include, path

from comments.views import CaptchaView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/comments/", include("comments.urls")),
    path("api/captcha/", CaptchaView.as_view(), name="captcha"),
]
