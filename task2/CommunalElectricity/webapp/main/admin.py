from django.contrib import admin
from .models import User, Bill, Meter, Reading

admin.site.register(User)
admin.site.register(Meter)
admin.site.register(Reading)
admin.site.register(Bill)


