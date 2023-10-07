from django.contrib import admin

# Register your models here.
from .models import Player, Active, Factor, Admin

admin.site.register(Player)
admin.site.register(Active)
admin.site.register(Factor)
admin.site.register(Admin)
