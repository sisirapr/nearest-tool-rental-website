from django.contrib import admin
from .models import Profile,RequestTool,ReplayTool,Contract
# Register your models here.

admin.site.register(Profile)
admin.site.register(RequestTool)
admin.site.register(ReplayTool)
admin.site.register(Contract)