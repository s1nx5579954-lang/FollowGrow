from django.contrib import admin
from .models import MonthlyList

class MonthlyListAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'user')

admin.site.register(MonthlyList, MonthlyListAdmin)