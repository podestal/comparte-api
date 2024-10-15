from django.contrib import admin
from . import models

admin.site.register(models.Service)
admin.site.register(models.StreamingServiceAccount)
admin.site.register(models.ScreenSubscription)
