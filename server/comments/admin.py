from django.contrib import admin

from .models import Attachment, Comment

admin.site.register(Comment)
admin.site.register(Attachment)
