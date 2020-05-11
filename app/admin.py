from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Card)
admin.site.register(Project)
admin.site.register(Plan)
admin.site.register(Subscription)
