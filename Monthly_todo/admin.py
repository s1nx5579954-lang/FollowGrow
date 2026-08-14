from django.contrib import admin
from .models import MonthlyList, MonthlyTask


class MonthlyTaskInline(admin.TabularInline):
    model = MonthlyTask
    extra = 1


class MonthlyListAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'user')
    inlines = [MonthlyTaskInline]


admin.site.register(MonthlyList, MonthlyListAdmin)