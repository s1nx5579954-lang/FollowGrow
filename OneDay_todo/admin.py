from django.contrib import admin

from .models import OneDayList, OneDayTask

class OneDayTaskInline(admin.TabularInline):
    model = OneDayTask
    extra = 1

class OneDayListAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [OneDayTaskInline]

admin.site.register(OneDayList, OneDayListAdmin)