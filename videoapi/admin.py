from django.contrib import admin
from videoapi.models import ApiKey,Query,Video,Channel


admin.site.register(ApiKey)
admin.site.register(Query)
admin.site.register(Video)
admin.site.register(Channel)

# Register your models here.
